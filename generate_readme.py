import json
import re
from pathlib import Path

data = json.loads(Path("stats.json").read_text())

# Icons shown either side of each game's heading
GAME_ICONS = {
    "Deadlock": "https://cdn.fastly.steamstatic.com/apps/deadlock/images/react/oldgods/rem_helper.png?2",
    "Overwatch": "https://cdn.fastly.steamstatic.com/apps/deadlock/images/react/oldgods/rem_helper.png?2",
}

# Colored/styled heading text for each game
GAME_HEADINGS = {
    "Deadlock": '<span style="color:#eedfbf">Deadlock</span>',
    "Overwatch": 'Ove<span style="color:#2596be">rwa</span>tch',
}

# Heroes shown in a sub-table under each game, sorted by total games played
GAME_HEROES = {
    "Deadlock": ["Celeste", "Silver", "Paige", "Ivy"],
    "Overwatch": ["D.Va", "Lucio", "Freja", "Symmetra"],
}

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
    "D.Va": {
        "gloat": "https://cdn3.emoji.gg/emojis/5341-dvapeace.png",
        "critical": "https://cdn3.emoji.gg/emojis/2766-dvamad.png",
    },
    "Lucio": {
        "gloat": "https://cdn3.emoji.gg/emojis/8866-luciocool.png",
        "critical": "https://cdn.betterttv.net/emote/5bc3e33f555f4b166afde06d/3x.webp",
    },
    "Freja": {
        "gloat": "https://i.pinimg.com/736x/31/33/7a/31337adb5d3962e15a2c2ad9fe3856dc.jpg",
        "critical": "https://i.pinimg.com/736x/3e/22/9f/3e229f35064784743b6a4442b75ebce1.jpg",
    },
    "Symmetra": {
        "gloat": "https://cdn3.emoji.gg/emojis/8861-symmetragiggle.png",
        "critical": "https://cdn3.emoji.gg/emojis/6694-symmetrasigh.png",
    },
}


def total_games(g):
    return g["wins"] + g["losses"]


def wr(g):
    t = total_games(g)
    return (g["wins"] / t * 100) if t else 0


def hero_image(hero, g):
    key = "gloat" if wr(g) >= 50 else "critical"
    return HERO_IMAGES[hero][key]


def game_heading(name):
    icon = GAME_ICONS[name]
    heading = GAME_HEADINGS[name]
    return f'### <img src="{icon}" height="22"> {heading} <img src="{icon}" height="22">'


def game_section(name, g):
    return (
        f"{game_heading(name)}\n"
        f"- Wins: {g['wins']}\n"
        f"- Losses: {g['losses']}\n"
        f"- Win Rate: {wr(g):.1f}%"
    )


def hero_table(name):
    heroes_sorted = sorted(GAME_HEROES[name], key=lambda h: total_games(data[h]), reverse=True)

    header_cells = []
    image_cells = []
    stats_cells = []
    for hero in heroes_sorted:
        g = data[hero]
        img = hero_image(hero, g)
        header_cells.append(hero)
        image_cells.append(f'<img src="{img}" width="60">')
        stats_cells.append(f"{g['wins']}W - {g['losses']}L ({wr(g):.1f}%)")

    table = (
        "#### Heroes\n"
        "| " + " | ".join(header_cells) + " |\n"
        "|" + "|".join(["---"] * len(header_cells)) + "|\n"
        "| " + " | ".join(image_cells) + " |\n"
        "| " + " | ".join(stats_cells) + " |"
    )
    return table


sections = []

for game in ["Deadlock", "Overwatch"]:
    sections.append(game_section(game, data[game]))
    sections.append(hero_table(game))

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
