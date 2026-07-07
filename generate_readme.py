
import json
import re
from pathlib import Path

# Load stats
data = json.loads(Path("stats.json").read_text())


GAME_ICONS = {
    "Deadlock": "https://cdn.fastly.steamstatic.com/apps/deadlock/images/react/oldgods/rem_helper.png?2",
    "Overwatch": "https://cdn.betterttv.net/emote/698afc803df753bf3f83fcbd/3x.webp",
}


GAME_HEADINGS = {
    "Deadlock": "Deadlock",
    "Overwatch": "Overwatch",
}


GAME_HEROES = {
    "Deadlock": ["Celeste", "Silver", "Paige", "Mina"],
    "Overwatch": ["D.Va", "Lucio", "Freja", "Symmetra"],
}


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
    "Mina": {
        "gloat": "https://deadlock.wiki/images/5/5e/Mina_Gloat.png",
        "critical": "https://deadlock.wiki/images/e/e3/Mina_Critical.png",
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


def win_rate(g):
    games = total_games(g)
    return (g["wins"] / games * 100) if games else 0


def hero_image(hero, stats):
    mood = "gloat" if win_rate(stats) >= 50 else "critical"
    return HERO_IMAGES[hero][mood]


def game_section(name, stats):
    icon = GAME_ICONS[name]
    heading = GAME_HEADINGS[name]

    heading_html = (
        f'<h3 align="center">'
        f'<img src="{icon}" height="22"> '
        f'{heading} '
        f'<img src="{icon}" height="22">'
        f'</h3>'
    )

    stats_html = (
        f'<p align="center">'
        f'Wins: {stats["wins"]}<br>'
        f'Losses: {stats["losses"]}<br>'
        f'Win Rate: {win_rate(stats):.1f}%'
        f'</p>'
    )

    heroes_sorted = sorted(
        GAME_HEROES[name],
        key=lambda h: total_games(data.get(h, {"wins": 0, "losses": 0})),
        reverse=True,
    )

    headers = []
    images = []
    results = []

    for hero in heroes_sorted:
        hero_stats = data.get(hero, {"wins": 0, "losses": 0})

        headers.append(hero)

        images.append(
            f'<img src="{hero_image(hero, hero_stats)}" width="60">'
        )

        results.append(
            f'{hero_stats["wins"]}W - '
            f'{hero_stats["losses"]}L '
            f'({win_rate(hero_stats):.1f}%)'
        )

    table = (
        "| " + " | ".join(headers) + " |\n"
        "|" + "|".join([":---:"] * len(headers)) + "|\n"
        "| " + " | ".join(images) + " |\n"
        "| " + " | ".join(results) + " |"
    )

    return (
        f"{heading_html}\n\n"
        f"{stats_html}\n\n"
        f"<h4 align=\"center\">Heroes</h4>\n\n"
        f"{table}"
    )


sections = [
    game_section("Deadlock", data["Deadlock"]),
    game_section("Overwatch", data["Overwatch"]),
]


stats_block = (
    "<!-- STATS_START -->\n"
    "# Stats\n\n"
    + "\n\n".join(sections)
    + "\n<!-- STATS_END -->"
)


readme_path = Path("README.md")
readme = readme_path.read_text()


if "<!-- STATS_START -->" in readme:
    readme = re.sub(
        r"<!-- STATS_START -->.*?<!-- STATS_END -->",
        stats_block,
        readme,
        flags=re.DOTALL,
    )
else:
    readme += "\n\n" + stats_block


readme_path.write_text(readme)
