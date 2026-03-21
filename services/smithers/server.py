"""
Smithers — Personal assistant webhook server.

Receives messages from Slack and Telegram, routes them through
Smithers' routing logic, and replies in the originating channel.
"""

import json
import os
import logging
import pathlib
import httpx
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("smithers")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SECRETS_DIR = pathlib.Path.home() / ".openclaw" / "workspace" / "secrets"
TELEGRAM_TOKEN_PATH = SECRETS_DIR / "telegram-bot-token.txt"
SLACK_TOKEN_PATH = SECRETS_DIR / "slack-bot-token.txt"

# Igwana's Telegram chat_id — set to None until first message is received.
# Once the first message arrives, it is written to disk so subsequent restarts
# remember it.
ALLOWED_CHAT_ID_PATH = SECRETS_DIR / "telegram-allowed-chat-id.txt"

SYSTEM_PROMPT_PATH = pathlib.Path(__file__).parent / "system-prompt.md"

# Tunnel / public URL (used for webhook registration)
TUNNEL_URL = os.environ.get("SMITHERS_TUNNEL_URL", "https://smithers.nikoskatsaounis.com")

# Slack webhook URL for cross-posting when a task needs Slack action
SLACK_WEBHOOK_URL = os.environ.get("SMITHERS_SLACK_WEBHOOK_URL", "")


def _read_secret(path: pathlib.Path) -> str | None:
    try:
        return path.read_text().strip()
    except FileNotFoundError:
        return None


def _get_telegram_token() -> str | None:
    return _read_secret(TELEGRAM_TOKEN_PATH)


def _get_slack_token() -> str | None:
    return _read_secret(SLACK_TOKEN_PATH)


def _get_allowed_chat_id() -> int | None:
    val = _read_secret(ALLOWED_CHAT_ID_PATH)
    if val is not None:
        try:
            return int(val)
        except ValueError:
            return None
    return None


def _save_allowed_chat_id(chat_id: int) -> None:
    ALLOWED_CHAT_ID_PATH.parent.mkdir(parents=True, exist_ok=True)
    ALLOWED_CHAT_ID_PATH.write_text(str(chat_id))
    log.info("Saved allowed Telegram chat_id: %s", chat_id)


def _load_system_prompt() -> str:
    try:
        return SYSTEM_PROMPT_PATH.read_text()
    except FileNotFoundError:
        return "You are Smithers, a personal executive assistant."


# ---------------------------------------------------------------------------
# Core routing logic (shared between Slack and Telegram)
# ---------------------------------------------------------------------------

def route_message(text: str) -> dict:
    """Route an incoming message through Smithers' logic.

    Returns a dict with:
        reply        — the text to send back to the user
        slack_action — optional dict with channel + message to cross-post to Slack
    """
    text_lower = text.strip().lower()

    # --- Quick commands ---
    if text_lower in ("ping", "hello", "hi"):
        return {"reply": "At your service, sir. How may I assist you today?"}

    if text_lower == "status":
        return {
            "reply": (
                "*Smithers Status Report*\n\n"
                "- Server: running\n"
                f"- Tunnel: `{TUNNEL_URL}`\n"
                f"- Telegram token: {'configured' if _get_telegram_token() else 'MISSING'}\n"
                f"- Slack token: {'configured' if _get_slack_token() else 'not configured'}\n"
                f"- Allowed chat\\_id: `{_get_allowed_chat_id() or 'any (first message claims)'}`"
            ),
        }

    # --- Task routing ---
    # Messages starting with specific prefixes get routed to Slack channels
    slack_action = None

    if text_lower.startswith("task:") or text_lower.startswith("todo:"):
        slack_action = {
            "channel": "#tasks",
            "message": text,
        }
        reply = f"Noted. I've logged this task and forwarded it to Slack.\n\n> {text}"

    elif text_lower.startswith("note:") or text_lower.startswith("memo:"):
        slack_action = {
            "channel": "#notes",
            "message": text,
        }
        reply = f"Memo recorded and posted to Slack.\n\n> {text}"

    elif text_lower.startswith("urgent:") or text_lower.startswith("alert:"):
        slack_action = {
            "channel": "#alerts",
            "message": f"🚨 {text}",
        }
        reply = f"*URGENT* — I've flagged this and posted to the alerts channel.\n\n> {text}"

    elif text_lower.startswith("slack:"):
        # Forward the rest of the message to a Slack channel
        parts = text[6:].strip().split(" ", 1)
        channel = parts[0] if parts else "#general"
        message = parts[1] if len(parts) > 1 else ""
        if not channel.startswith("#"):
            channel = f"#{channel}"
        slack_action = {
            "channel": channel,
            "message": message,
        }
        reply = f"Posted to Slack `{channel}`:\n> {message}"

    else:
        # Default: echo-acknowledge — in production this would call an LLM
        reply = (
            f"Received your message:\n\n"
            f"> {text}\n\n"
            "I'll process this and follow up. "
            "Prefix with `task:`, `note:`, `urgent:`, or `slack:#channel` "
            "for specific routing."
        )

    result = {"reply": reply}
    if slack_action:
        result["slack_action"] = slack_action
    return result


# ---------------------------------------------------------------------------
# Slack helpers
# ---------------------------------------------------------------------------

def post_to_slack(channel: str, message: str) -> bool:
    """Post a message to Slack via Incoming Webhook or Bot API."""
    if SLACK_WEBHOOK_URL:
        try:
            r = httpx.post(
                SLACK_WEBHOOK_URL,
                json={"channel": channel, "text": message},
                timeout=10,
            )
            r.raise_for_status()
            return True
        except Exception as exc:
            log.error("Slack post failed: %s", exc)
            return False

    token = _get_slack_token()
    if not token:
        log.warning("No Slack token configured — skipping Slack post")
        return False

    try:
        r = httpx.post(
            "https://slack.com/api/chat.postMessage",
            headers={"Authorization": f"Bearer {token}"},
            json={"channel": channel, "text": message},
            timeout=10,
        )
        data = r.json()
        if not data.get("ok"):
            log.error("Slack API error: %s", data.get("error"))
            return False
        return True
    except Exception as exc:
        log.error("Slack post failed: %s", exc)
        return False


# ---------------------------------------------------------------------------
# Telegram helpers
# ---------------------------------------------------------------------------

def send_telegram_message(chat_id: int, text: str, parse_mode: str = "Markdown") -> bool:
    """Send a message via the Telegram Bot API."""
    token = _get_telegram_token()
    if not token:
        log.error("Telegram bot token not configured at %s", TELEGRAM_TOKEN_PATH)
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    }

    try:
        r = httpx.post(url, json=payload, timeout=10)
        data = r.json()
        if not data.get("ok"):
            log.error("Telegram API error: %s", data)
            # Retry without parse_mode in case of Markdown formatting issues
            if parse_mode:
                log.info("Retrying without parse_mode...")
                payload.pop("parse_mode")
                r = httpx.post(url, json=payload, timeout=10)
                data = r.json()
                if not data.get("ok"):
                    log.error("Telegram API error (retry): %s", data)
                    return False
            else:
                return False
        return True
    except Exception as exc:
        log.error("Telegram send failed: %s", exc)
        return False


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "smithers"})


@app.route("/slack/smithers", methods=["POST"])
def slack_webhook():
    """Handle incoming Slack webhook events."""
    data = request.json or {}

    # Slack URL verification challenge
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # Extract message text
    event = data.get("event", {})
    text = event.get("text", "")
    channel = event.get("channel", "")
    user = event.get("user", "")

    if not text:
        return jsonify({"ok": True})

    # Ignore bot messages to prevent loops
    if event.get("bot_id") or event.get("subtype") == "bot_message":
        return jsonify({"ok": True})

    log.info("Slack message from %s in %s: %s", user, channel, text[:100])

    result = route_message(text)

    # Handle Slack action cross-posting
    if result.get("slack_action"):
        action = result["slack_action"]
        post_to_slack(action["channel"], action["message"])

    # Reply in the originating Slack channel
    token = _get_slack_token()
    if token:
        try:
            httpx.post(
                "https://slack.com/api/chat.postMessage",
                headers={"Authorization": f"Bearer {token}"},
                json={"channel": channel, "text": result["reply"]},
                timeout=10,
            )
        except Exception as exc:
            log.error("Slack reply failed: %s", exc)

    return jsonify({"ok": True})


@app.route("/telegram/webhook", methods=["POST"])
def telegram_webhook():
    """Handle incoming Telegram webhook updates.

    Flow:
    1. Parse the update — extract chat_id and message text.
    2. Gate on allowed chat_id (auto-claim on first message if not set).
    3. Route through the shared Smithers routing logic.
    4. Send reply back to Telegram.
    5. Cross-post to Slack if the route requires it.
    """
    update = request.json or {}

    # Telegram sends various update types; we only care about messages with text
    message = update.get("message") or update.get("edited_message")
    if not message:
        return jsonify({"ok": True})

    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")
    from_user = message.get("from", {})
    username = from_user.get("username", "unknown")
    first_name = from_user.get("first_name", "")

    if not text or not chat_id:
        return jsonify({"ok": True})

    log.info(
        "Telegram message from @%s (%s) [chat_id=%s]: %s",
        username, first_name, chat_id, text[:100],
    )

    # --- Chat ID gating ---
    allowed = _get_allowed_chat_id()
    if allowed is None:
        # First message claims this chat_id
        _save_allowed_chat_id(chat_id)
        send_telegram_message(
            chat_id,
            f"Welcome, {first_name}. I've registered your chat\\_id (`{chat_id}`) "
            "as the authorized user. All future messages from other chats will be ignored.\n\n"
            "How may I assist you, sir?",
        )
        return jsonify({"ok": True})

    if chat_id != allowed:
        log.warning(
            "Ignoring message from unauthorized chat_id %s (allowed: %s)",
            chat_id, allowed,
        )
        return jsonify({"ok": True})

    # --- Route the message ---
    result = route_message(text)

    # --- Send reply to Telegram ---
    send_telegram_message(chat_id, result["reply"])

    # --- Cross-post to Slack if needed ---
    if result.get("slack_action"):
        action = result["slack_action"]
        success = post_to_slack(action["channel"], action["message"])
        if success:
            send_telegram_message(chat_id, f"_Also posted to Slack {action['channel']}_")
        else:
            send_telegram_message(
                chat_id,
                "⚠️ _Slack cross-post failed — check Slack token configuration._",
            )

    return jsonify({"ok": True})


# ---------------------------------------------------------------------------
# Webhook registration endpoint (convenience)
# ---------------------------------------------------------------------------

@app.route("/telegram/register-webhook", methods=["POST"])
def register_telegram_webhook():
    """Register this server's URL as the Telegram webhook.

    Call this once after the tunnel is up:
        curl -X POST http://localhost:5055/telegram/register-webhook
    """
    token = _get_telegram_token()
    if not token:
        return jsonify({
            "ok": False,
            "error": f"Bot token not found at {TELEGRAM_TOKEN_PATH}",
        }), 500

    webhook_url = f"{TUNNEL_URL.rstrip('/')}/telegram/webhook"

    try:
        r = httpx.post(
            f"https://api.telegram.org/bot{token}/setWebhook",
            json={"url": webhook_url, "allowed_updates": ["message", "edited_message"]},
            timeout=10,
        )
        data = r.json()
        log.info("Telegram setWebhook response: %s", data)
        return jsonify({"ok": data.get("ok"), "webhook_url": webhook_url, "response": data})
    except Exception as exc:
        log.error("setWebhook failed: %s", exc)
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/telegram/webhook-info", methods=["GET"])
def telegram_webhook_info():
    """Check current Telegram webhook status."""
    token = _get_telegram_token()
    if not token:
        return jsonify({"ok": False, "error": "Bot token not configured"}), 500

    try:
        r = httpx.get(f"https://api.telegram.org/bot{token}/getWebhookInfo", timeout=10)
        return jsonify(r.json())
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("SMITHERS_PORT", 5055))
    log.info("Starting Smithers on port %d", port)
    log.info("Telegram token: %s", "configured" if _get_telegram_token() else "MISSING")
    log.info("Tunnel URL: %s", TUNNEL_URL)
    app.run(host="0.0.0.0", port=port, debug=True)
