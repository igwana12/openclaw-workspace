# OpenClaw Skills Index

> Master index of all 38 skills available in the AI OS.
> Source: `/Volumes/Extreme Pro/SKILLS/`
> Registry: `skills/registry.json`

## Trading Skills (16 production skills)

Source: `/Volumes/Extreme Pro/SKILLS/trading-claude/`

| Skill | Category | Scripts | API | Status |
|-------|----------|---------|-----|--------|
| [backtest-expert](trading/backtest-expert.md) | Backtesting | - | - | production |
| [breadth-chart-analyst](trading/breadth-chart-analyst.md) | Market Analysis | - | - | production |
| [dividend-growth-pullback-screener](trading/dividend-growth-pullback-screener.md) | Screening | `screen_dividend_growth_rsi.py` | FMP | production |
| [earnings-calendar](trading/earnings-calendar.md) | Data Fetching | `fetch_earnings_fmp.py`, `generate_report.py` | FMP | production |
| [economic-calendar-fetcher](trading/economic-calendar-fetcher.md) | Data Fetching | `get_economic_calendar.py` | FMP | production |
| [institutional-flow-tracker](trading/institutional-flow-tracker.md) | Flow Analysis | `analyze_single_stock.py`, `track_*.py` | - | production |
| [market-environment-analysis](trading/market-environment-analysis.md) | Market Analysis | `market_utils.py` | - | production |
| [market-news-analyst](trading/market-news-analyst.md) | News Analysis | - | - | production |
| [options-strategy-advisor](trading/options-strategy-advisor.md) | Options | `black_scholes.py` | - | production |
| [pair-trade-screener](trading/pair-trade-screener.md) | Screening | `analyze_spread.py`, `find_pairs.py` | - | production |
| [portfolio-manager](trading/portfolio-manager.md) | Portfolio | `test_alpaca_connection.py` | Alpaca | production |
| [sector-analyst](trading/sector-analyst.md) | Sector Analysis | - | - | production |
| [stanley-druckenmiller-investment](trading/stanley-druckenmiller-investment.md) | Strategy | - | - | production |
| [technical-analyst](trading/technical-analyst.md) | Technical Analysis | - | - | production |
| [us-market-bubble-detector](trading/us-market-bubble-detector.md) | Risk Analysis | `bubble_scorer.py` | - | production |
| [us-stock-analysis](trading/us-stock-analysis.md) | Stock Analysis | - | - | production |
| [value-dividend-screener](trading/value-dividend-screener.md) | Screening | `screen_dividend_stocks.py` | FMP | production |

## Trading Agents (5)

| Agent | Skills Used |
|-------|------------|
| druckenmiller-strategy-planner | stanley-druckenmiller-investment |
| market-news-analyzer | market-news-analyst |
| technical-market-analyst | technical-analyst, breadth-chart-analyst |
| us-market-analyst | us-market-bubble-detector, market-environment-analysis |
| weekly-trade-blog-writer | all (Japanese output) |

## General Skills (22 from jamesrochabrun collection)

Source: `/Volumes/Extreme Pro/SKILLS/trading-plugins/jamesrochabrun-skills/`

| Skill | Category | Status |
|-------|----------|--------|
| [anthropic-architect](general/anthropic-architect.md) | AI / Architecture | reference |
| [anthropic-prompt-engineer](general/anthropic-prompt-engineer.md) | AI / Prompting | reference |
| [apple-hig-designer](general/apple-hig-designer.md) | Design / iOS | reference |
| [book-illustrator](general/book-illustrator.md) | Content / Visual | reference |
| [content-brief-generator](general/content-brief-generator.md) | Content / Marketing | reference |
| [design-brief-generator](general/design-brief-generator.md) | Design / UX | reference |
| [engineer-expertise-extractor](general/engineer-expertise-extractor.md) | Meta / Skills | reference |
| [engineer-skill-creator](general/engineer-skill-creator.md) | Meta / Skills | reference |
| [frontend-designer](general/frontend-designer.md) | Development / UI | reference |
| [git-worktrees](general/git-worktrees.md) | Development / Git | reference |
| [kids-book-writer](general/kids-book-writer.md) | Content / Writing | reference |
| [leetcode-teacher](general/leetcode-teacher.md) | Education / CS | reference |
| [llm-router](general/llm-router.md) | AI / Orchestration | reference |
| [math-teacher](general/math-teacher.md) | Education / Math | reference |
| [openai-prompt-engineer](general/openai-prompt-engineer.md) | AI / Prompting | reference |
| [prd-generator](general/prd-generator.md) | Product / Planning | reference |
| [qa-test-planner](general/qa-test-planner.md) | Development / QA | reference |
| [query-expert](general/query-expert.md) | Development / Database | reference |
| [reading-teacher](general/reading-teacher.md) | Education / Reading | reference |
| [technical-launch-planner](general/technical-launch-planner.md) | Product / Launch | reference |
| [trading-plan-generator](general/trading-plan-generator.md) | Trading / Strategy | reference |

## Priority Skills for OpenClaw

### Immediate Use
- **anthropic-prompt-engineer** - Improve the prompt library
- **anthropic-architect** - Architecture patterns for AI systems
- **engineer-skill-creator** - Meta-skill for creating new skills
- **engineer-expertise-extractor** - Extract expertise into skills
- **llm-router** - Pairs with llm-router project in ACTIVE

### Content Pipeline
- **content-brief-generator** - Sacred Circuits content
- **kids-book-writer** - Book projects
- **book-illustrator** - Visual direction

### Trading Operations
- **portfolio-manager** - Full portfolio management via Alpaca
- **weekly-trade-strategy** (workflow) - Automated weekly analysis

## Empty Directories (Future Use)
- `anthropic/` - Reserved for Anthropic-specific skills
- `business/` - Reserved for business operation skills
- `internals/` - Reserved for internal system skills
- `trading/` - Reserved for general trading skills
