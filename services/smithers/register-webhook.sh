#!/usr/bin/env bash
# Register the Telegram webhook with the bot API.
#
# Usage:
#   ./register-webhook.sh                          # uses default tunnel URL
#   SMITHERS_TUNNEL_URL=https://... ./register-webhook.sh  # override URL
#
# Or just hit the local endpoint:
#   curl -X POST http://localhost:5055/telegram/register-webhook

set -euo pipefail

SECRETS_DIR="${HOME}/.openclaw/workspace/secrets"
TOKEN_FILE="${SECRETS_DIR}/telegram-bot-token.txt"

if [[ ! -f "$TOKEN_FILE" ]]; then
    echo "ERROR: Telegram bot token not found at $TOKEN_FILE"
    echo ""
    echo "To set up:"
    echo "  1. Talk to @BotFather on Telegram"
    echo "  2. Create a bot or get the token for an existing one"
    echo "  3. Save it:  echo 'YOUR_TOKEN' > $TOKEN_FILE"
    exit 1
fi

TOKEN=$(cat "$TOKEN_FILE" | tr -d '[:space:]')
TUNNEL_URL="${SMITHERS_TUNNEL_URL:-https://smithers.nikoskatsaounis.com}"
WEBHOOK_URL="${TUNNEL_URL}/telegram/webhook"

echo "Registering Telegram webhook..."
echo "  Bot token: ${TOKEN:0:10}..."
echo "  Webhook URL: $WEBHOOK_URL"
echo ""

RESPONSE=$(curl -s -X POST \
    "https://api.telegram.org/bot${TOKEN}/setWebhook" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"${WEBHOOK_URL}\", \"allowed_updates\": [\"message\", \"edited_message\"]}")

echo "Response: $RESPONSE"

echo ""
echo "Checking webhook info..."
curl -s "https://api.telegram.org/bot${TOKEN}/getWebhookInfo" | python3 -m json.tool
