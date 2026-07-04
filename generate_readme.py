import json
import re
from pathlib import Path

data = json.loads(Path("stats.json").read_text())

# Top-level games shown as their own section
TOP_LEVEL_GAMES = ["Overwatch"]

# Deadlock heroes shown in a table under the Deadlock section
DEADLOCK_HEROES = ["Celeste", "Silver", "Paige", "Ivy"]

# Portrait shown depending on whether the hero's win rate is
# above/at 50% ("gloat") or below 50% ("critical")
HERO_IMAGES = {
    "Celeste": {
        "gloat": "https://deadlock.wiki/images/7/70/Celeste_Gloat.png",
        "critical": "https://deadlock.wiki/images/4/41/Celeste_Critical_Health.png",
    },
    "Paige": {
        "gloat": "https://deadlock.wiki/images/9/9f/Paige_Gloat.png",
        "critical": "https://deadlock.wiki/images/0/02/Paige_Critical.png",
    },
    "Silver": {
        "gloat": "https://deadlock.wiki/images/4/44/Silver_Gloat_Portrait.png",
        "critical": "https://deadlock.wiki/images/8/8b/Silver_Critical_Health.png",
    },
    "Ivy": {
        "gloat": "https://deadlock.wiki/images/4/45/Ivy_Gloat_.png",
        "critical": "https://deadlock.wiki/images/3/37/Ivy_Critical_.png",
    },
}


def total_games(g):
    return g["wins"] + g["losses"]


def wr(g):
    t = total_games(g)
    return (g["wins"] / t * 100) if t else 0


def hero_image(hero, g):
    rate = wr(g)
    key = "gloat" if rate >= 50 else "critical"
    return HERO_IMAGES[hero][key]


def game_section(name, g):
    return (
        f"### {name}\n"
        f"- Wins: {g['wins']}\n"
        f"- Losses: {g['losses']}\n"
        f"- Win Rate: {wr(g):.1f}%"
    )


sections = []

# Deadlock section (with hero sub-table), always first
deadlock = data["Deadlock"]
sections.append(game_section("Deadlock", deadlock))

heroes_sorted = sorted(DEADLOCK_HEROES, key=lambda h: total_games(data[h]), reverse=True)

header_cells = []
image_cells = []
stats_cells = []
for hero in heroes_sorted:
    g = data[hero]
    img = hero_image(hero, g)
    header_cells.append(hero)
    image_cells.append(f'<img src="{img}" width="60">')
    stats_cells.append(f"{g['wins']}W - {g['losses']}L ({wr(g):.1f}%)")

hero_table = (
    "#### Heroes\n"
    "| " + " | ".join(header_cells) + " |\n"
    "|" + "|".join(["---"] * len(header_cells)) + "|\n"
    "| " + " | ".join(image_cells) + " |\n"
    "| " + " | ".join(stats_cells) + " |\n"
)
sections.append(hero_table.rstrip("\n"))

# Remaining top-level games
for game in TOP_LEVEL_GAMES:
    sections.append(game_section(game, data[game]))

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
