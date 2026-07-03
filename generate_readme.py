import json
from pathlib import Path

data = json.loads(Path("stats.json").read_text())

def wr(g):
    return g["wins"] / (g["wins"] + g["losses"]) * 100 if (g["wins"] + g["losses"]) else 0

output = f"""## 🎮 Game Stats

### Deadlock
- Wins: {data['Deadlock']['wins']}
- Losses: {data['Deadlock']['losses']}
- Win Rate: {wr(data['Deadlock']):.1f}%

### Overwatch
- Wins: {data['Overwatch']['wins']}
- Losses: {data['Overwatch']['losses']}
- Win Rate: {wr(data['Overwatch']):.1f}%
"""

Path("STATS.md").write_text(output)
