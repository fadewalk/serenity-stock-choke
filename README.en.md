# Serenity Stock Choke · A-Share / HK / US Choke-Point Stock Picking Framework

<p align="center"><b>English</b> · <a href="README.md">简体中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a></p>

> "**Trace the supply chain upstream to the node where, if it ever runs dry, a trillion-dollar industry grinds to a halt — the small caps sitting on that node are the next big strike.**"

This Skill applies the supply-chain bottleneck theory of Reddit legend **Serenity (@aleabitoreddit)** across **A-shares, Hong Kong and US markets**, forming a universal industry-chain analysis framework. Serenity's original trades were US stocks (AXTI, AAOI); the A-share version is the localized adaptation.

---

## Core Methodology

### The Strait of Hormuz Analogy

> "The Strait of Hormuz is the throat of global oil. Block it, and everyone suffers. But if you own equity in the Strait of Hormuz itself, you own pricing power."

**Translated to investing**: which node is the "Hormuz" of a major track — and which listed companies (A-share / HK / US) control it?

### Three-Step Core Logic

```
① AI boom / policy drive / technology leapfrogging
    ↓
② Upstream hardware & materials demand explodes; some supply-chain nodes can't keep up
    ↓
③ The bottleneck node gains pricing power → small caps there have the most torque
```

### Serenity's Original Track Record (US)

| Stock | Ticker | Choke-point position |
|------|--------|---------------------|
| AXT Inc | AXTI.US | One of only ~3 global InP substrate makers |
| Applied Optoelectronics | AAOI.US | Key CPO laser supplier |
| Sivers Semiconductors | SIVE.SE | CPO lasers + silicon photonics |
| X-FAB | XFAB.EU | Specialty-process foundry |

> ⚠️ The table above is a **survivorship-biased, ex-post sample** used to illustrate the framework only. It does not represent the expected return of the framework.

---

## Six-Step Analysis Pipeline

| Step | Question | Output |
|------|---------|--------|
| 1️⃣ Cycle stage | Demand explosion / tech leapfrog / supply constrained? | Sector stage |
| 2️⃣ Trace supply chain | Which layer is the bottleneck? | Supply-chain map |
| 3️⃣ Find listed names | Who sits on the node? (A/HK/US) | Four-factor signal card |
| 4️⃣ True vs fake | Real bottleneck or hot-money riding? | Screening verdict (7 exclusion rules) |
| 5️⃣ Two-sided check | Bull vs bear signals? | Signal table |
| 6️⃣ Report | Position sizing + risk | Structured report (8 sections) |

---

## Supported Markets

| Market | Quote/valuation (`stock`/`search`) | Sector K-line | Reports/margin/chips |
|------|:---:|:---:|:---:|
| **A-share** | ✅ incl. main fund flow | ✅ | ✅ |
| **Hong Kong** | ✅ HKD | — | web-search fallback |
| **US** | ✅ USD, Chinese name lookup | — | web-search fallback |

The six-step framework itself is market-agnostic. For HK/US institutional signals (13F, short interest, southbound flow, short-selling ratio), use the search templates in SKILL.md. Note: 13F lags 45 days (quarterly); short interest is bi-weekly.

---

## Quick Start

### Install (pick one)

**Option 0 — paste one message to your AI agent (easiest).** Give the text below to Claude Code / Codex / any agent that can run commands, and it will install and verify itself:

```
Install the skill at https://github.com/fadewalk/serenity-stock-choke :
clone it into this agent's skills directory (Claude Code: ~/.claude/skills/,
other agents: .agents/skills/; if unsure, follow the repo README), then verify
with python3 <skill-dir>/scripts/a_stock_query.py stock 600519 and tell me how
to invoke this skill and what it can do.
```

**Option 1 — Claude Code plugin marketplace:**

```
/plugin marketplace add fadewalk/serenity-stock-choke
/plugin install serenity-stock-choke@serenity-stock-choke
```

**Option 2 — skills.sh installer:**

```bash
npx skills add fadewalk/serenity-stock-choke
```

**Option 3 — manual clone:**

```bash
git clone https://github.com/fadewalk/serenity-stock-choke.git ~/.claude/skills/serenity-stock-choke
```

The bundled query script uses only the Python standard library — no dependencies, no API key (`akshare` optional: `pip install akshare`).

### How to Trigger

```
Use serenity-stock-choke to analyze [sector]
e.g. Use serenity-stock-choke to analyze the US AI compute supply chain
Find the choke points in [industry]
```

### Data Access (3-tier fallback, works in any environment)

1. **Agent's own finance tools** (MCP market-data/research tools) — prefer these if available
2. **Bundled script** (`scripts/a_stock_query.py`, zero-dependency, multi-source fallback):
   ```bash
   python3 scripts/a_stock_query.py stock 600519     # A-share snapshot: price/PE/PB/mcap/fund flow
   python3 scripts/a_stock_query.py stock 00700      # HK: Tencent (HKD)
   python3 scripts/a_stock_query.py stock AAPL       # US: Apple (USD)
   python3 scripts/a_stock_query.py valuation 600519 # A-share PE/PB historical percentile
   python3 scripts/a_stock_query.py kline 300308     # momentum / annualized vol / max drawdown
   python3 scripts/a_stock_query.py business 600519  # A-share revenue mix (hot-money check)
   python3 scripts/a_stock_query.py sector 电力       # A-share sector K-line
   python3 scripts/a_stock_query.py reports 600519   # A-share broker reports
   python3 scripts/a_stock_query.py margin 600519    # A-share margin balance
   ```
3. **Web-search fallback**: use the templates in SKILL.md for supply gaps, policy, chips, 13F, short interest, etc.

## File Structure

```
serenity-stock-choke/
├── SKILL.md                    # Main prompt (6-step pipeline + 3-tier data strategy)
├── README.md                   # 简体中文版
├── README.en.md                # This file
├── README.ja.md                # 日本語版
├── README.ko.md                # 한국어版
├── .claude-plugin/             # Claude Code plugin marketplace (one-click install)
├── scripts/
│   └── a_stock_query.py        # Standalone data script (zero-dep, multi-source, A/HK/US)
└── references/
    └── user_guide.md          # Usage guide + sector reference table (Chinese)
```

---

## Risk Disclosure

1. For research reference only. Not investment advice.
2. Small caps can swing 20-30% in a single day.
3. A-shares are heavily policy-driven; watch regulatory moves closely.
4. Supply-chain information is noisy; verify independently.
5. Thesis validation may take 1-3 years.

---

## References

- [yan-labs/serenity-aleabitoreddit](https://github.com/yan-labs/serenity-aleabitoreddit) — distillation of Serenity's tweets (2025-07 → 2026-09: 6,592 tweets + 4 articles, methodology + track record)
- [Original Serenity Skill (EN)](https://github.com/leslieyeo/aleabitoreddit-skill)
- [semiconstocks.com tracker](https://semiconstocks.com/zh)
- [Singularity Research Fund](https://singularityresearchfund.substack.com)
