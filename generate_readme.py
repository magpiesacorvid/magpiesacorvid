import json
import re
from pathlib import Path

data = json.loads(Path("stats.json").read_text())

# Order games appear in the README
GAMES = ["Deadlock", "Overwatch", "Celeste", "Silver", "Paige", "Ivy"]


def wr(g):
    total = g["wins"] + g["losses"]
    return (g["wins"] / total * 100) if total else 0


sections = []
for game in GAMES:
    g = data[game]
    sections.append(
        f"### {game}\n"
        f"- Wins: {g['wins']}\n"
        f"- Losses: {g['losses']}\n"
        f"- Win Rate: {wr(g):.1f}%"
    )

stats_block = "## Game Stats\n" + "\n".join(sections) + "\n"

readme_path = Path("README.md")
readme = readme_path.read_text()

new_readme = re.sub(
    r"<!-- START_STATS -->.*?<!-- END_STATS -->",
    f"<!-- START_STATS -->\n{stats_block}<!-- END_STATS -->",
    readme,
    flags=re.DOTALL,
)

readme_path.write_text(new_readme)
