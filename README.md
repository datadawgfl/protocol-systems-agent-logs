# Protocol Systems agent logs

Decision logs from the Protocol Systems trading agent, Oct 21 – Dec 21, 2026.

Claude reads the market, writes a signal, and records why. Code checks that signal against fixed risk rules. A person approves every trade. Once a week the agent reviews its own decisions and proposes changes, and a person decides which ones ship.

Every file in `decisions/` and `reflections/` is a real record from a real run. Nothing is backfilled, edited after the fact, or simulated without saying so. Losing trades stay in.

## How a decision flows

1. **Signal.** The agent pulls hourly OANDA data for the pairs on the Protocol V2 whitelist and writes a signal: direction, reasoning, and a confidence score.
2. **Risk gate (code).** The signal must pass rules written in code: whitelisted pair, Protocol V2 filter, position size, daily loss cap. The model's confidence score is logged and studied. It never places a trade on its own.
3. **Human approval.** Signals that pass the gate go to Telegram. A person taps approve or reject. Nothing executes without that tap.
4. **Outcome.** Fills, exits and P&L are written back to the same record.
5. **Weekly reflection.** The agent reviews the week, compares its confidence with what actually happened, and proposes adjustments. Accepted changes are listed in the reflection file.

## What's in here

| Folder | Contents |
| --- | --- |
| `decisions/` | One JSON file per signal, named `YYYY-MM-DD-PAIR-NNN.json`. Format: `examples/decision.example.json` |
| `reflections/` | One Markdown file per week, named `YYYY-week-NN.md`. Format: `examples/reflection.example.md` |
| `examples/` | Blank formats with made-up values. Not trades. |
| `scripts/scrub_check.py` | Run before every commit. Blocks account numbers, keys, webhook URLs and config files. |

## Rules this agent runs under

- A model's judgment never places a trade. Code gates execution, and a person approves it.
- Pocket Option is never automated.
- No promised returns. Results are shown as they happened, losses included.

## Before committing

```bash
python3 scripts/scrub_check.py
```

It exits non-zero and names the file and line if anything sensitive is staged.

## License

MIT. See `LICENSE`.

Built by Dez Lewis.
