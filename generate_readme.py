import json
from pathlib import Path

data = json.loads(Path("stats.json").read_text())


def wr(game):
    total = game["wins"] + game["losses"]
    return (game["wins"] / total * 100) if total else 0


lines = ["## Game Stats", ""]

for game, stats in data.items():
    lines.extend(
        [
            f"### {game}",
            "",
            f"- Wins: {stats['wins']}",
            f"- Losses: {stats['losses']}",
            f"- Win Rate: {wr(stats):.1f}%",
            "",
        ]
    )

output = "\n".join(lines)

Path("README.md").write_text(output)
