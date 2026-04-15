# 🐙 OSINT or Fiction?

> A terminal threat-intelligence game. Can you tell a malicious IP from a legitimate one?  
> Get 3 wrong and the kraken eats you.

Built for [MLH Global Hack Week: API Week 2026](https://ghw.mlh.io/events/api-week).  
Powered by the [AbuseIPDB](https://www.abuseipdb.com/) threat intelligence API.

---

## Gameplay

You're shown an IP address. You decide: **Malicious** or **Benign**?

- Every correct answer earns **10 points**
- 3+ correct answers in a row earns a **streak bonus**
- 3 wrong answers and the **kraken ascends** to eat you
- The kraken ASCII art gets progressively more menacing — and judgy — as you fail

Runs in **demo mode** (curated targets with flavor text) without an API key, or **live mode** against AbuseIPDB's real-time threat database with your own key.

---

## Setup

Requires Python 3.11+ and [`uv`](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/YOUR_USERNAME/osint-or-fiction
cd osint-or-fiction

# Install dependencies
uv sync

# Optional: add your AbuseIPDB API key for live mode
cp .env.example .env
# edit .env and add ABUSEIPDB_API_KEY=your_key_here
```

### Get a Free AbuseIPDB API Key
Register at [https://www.abuseipdb.com/register](https://www.abuseipdb.com/register).  
Free tier: **1,000 checks/day** — more than enough to lose repeatedly.

---

## Run

```bash
uv run python game.py
```

Or if you installed as a script:

```bash
uv run osint-or-fiction
```

---

## How It Works

In **live mode**, each IP is checked against the [AbuseIPDB `/v2/check` endpoint](https://docs.abuseipdb.com/#check-endpoint) in real time:

```
GET https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90
```

An IP with a **confidence score ≥ 25%** is classified as malicious. The threshold is intentionally not 100% — threat intel is messy, and "Googlebot" has reports too.

In **demo mode**, a curated set of 20 IPs is used — a mix of known-bad (Tor exits, C2 infrastructure, mass-scanners) and known-good (major DNS resolvers, CDN nodes, Google backbone). Flavor text is included to shame you appropriately.

---

## Project Structure

```
osint-or-fiction/
├── game.py        — main game loop + Rich UI
├── kraken.py      — ASCII art for all 4 stages of your doom
├── api.py         — AbuseIPDB client + demo target data
├── pyproject.toml — uv/hatch project config
├── .env.example   — API key template
└── README.md      — you are here
```

---

## Tech Stack

| Thing | Why |
|---|---|
| [AbuseIPDB API](https://www.abuseipdb.com/api) | Real threat intelligence — not vibes |
| [Rich](https://github.com/Textualize/rich) | Terminal UI with purple/cyan energy |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Because hardcoding API keys is a threat in itself |
| `uv` | Dependency management that doesn't require a therapy session |

---

## Contributing

PRs welcome. Especially:
- More IP targets with flavor text
- Additional kraken ASCII stages
- Leaderboard / high score persistence
- Domain-name mode (URLs instead of IPs)

---

*Built with spite and coffee during MLH API Week 2026.*  
*The kraken is not responsible for your incorrect guesses.*
