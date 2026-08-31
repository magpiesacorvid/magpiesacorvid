import json
import re
from pathlib import Path

# Load stats
data = json.loads(Path("stats.json").read_text())


GAME_ICONS = {
    "Deadlock": "https://cdn.fastly.steamstatic.com/apps/deadlock/images/react/oldgods/rem_helper.png?2",
}


GAME_HEADINGS = {
    "Deadlock": "Deadlock",
}


# Order here is the tie-break order used when two heroes have the same
# number of games played (sorted() is stable, so ties keep this order).
GAME_HEROES = {
    "Deadlock": [
        "Celeste",
        "Silver",
        "Paige",
        "Mina",
        "Vyper",
        "Ivy",
        "Holliday",
        "Graves",
        "Venator",
        "McGinnis",
        "Vindicta",
        "Mirage",
        "Wraith",
        "Abrams",
        "Dynamo",
        "Haze",
        "Infernus",
        "Calico",
        "Lady Geist",
        "Viscous",
        "Grey Talon",
        "Lash",
        "Paradox",
        "Pocket",
        "Rem",
    ],
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
    "Vyper": {
        "gloat": "https://iili.io/C0UOdB4.png",
        "critical": "https://iili.io/C0UOHQf.png",
    },
    "Ivy": {
        "gloat": "https://deadlock.wiki/images/4/45/Ivy_Gloat_.png",
        "critical": "https://deadlock.wiki/images/3/37/Ivy_Critical_.png",
    },
    "Holliday": {
        "gloat": "https://deadlock.wiki/images/4/46/Holliday_Gloat.png",
        "critical": "https://deadlock.wiki/images/7/7c/Holliday_Critical.png",
    },
    "Graves": {
        "gloat": "https://deadlock.wiki/images/f/ff/Graves_Gloat.png",
        "critical": "https://deadlock.wiki/images/0/06/Graves_Critical_Health.png",
    },
    "Venator": {
        "gloat": "https://deadlock.wiki/images/1/1b/Venator_Gloat.png",
        "critical": "https://deadlock.wiki/images/5/55/Venator_Critical_Health.png",
    },
    "McGinnis": {
        "gloat": "https://deadlock.wiki/images/7/7d/McGinnis_Gloat.png",
        "critical": "https://deadlock.wiki/images/7/7d/McGinnis_Critical.png",
    },
    "Vindicta": {
        "gloat": "https://deadlock.wiki/images/d/d0/Vindicta_Gloat.png",
        "critical": "https://deadlock.wiki/images/9/98/Vindicta_Critical.png",
    },
    "Mirage": {
        "gloat": "https://deadlock.wiki/images/9/99/Mirage_Gloat_.png",
        "critical": "https://deadlock.wiki/images/a/a3/Mirage_Critical.png",
    },
    "Wraith": {
        "gloat": "https://deadlock.wiki/images/4/48/Wraith_Gloat.png",
        "critical": "https://deadlock.wiki/images/6/6c/Wraith_Critical.png",
    },
    "Abrams": {
        "gloat": "https://deadlock.wiki/images/c/c1/Abrams_Gloat.png",
        "critical": "https://deadlock.wiki/images/4/4f/Abrams_Critical.png",
    },
    "Dynamo": {
        "gloat": "https://deadlock.wiki/images/9/9e/Dynamo_Gloat.png",
        "critical": "https://deadlock.wiki/images/1/19/Dynamo_Critical.png",
    },
    "Haze": {
        "gloat": "https://deadlock.wiki/images/d/d7/Haze_Gloat.png",
        "critical": "https://deadlock.wiki/images/c/c4/Haze_Critical.png",
    },
    "Infernus": {
        "gloat": "https://deadlock.wiki/images/9/91/Infernus_Gloat.png",
        "critical": "https://deadlock.wiki/images/8/8a/Infernus_Critical_.png",
    },
    "Calico": {
        "gloat": "https://deadlock.wiki/images/2/23/Calico_Gloat.png",
        "critical": "https://deadlock.wiki/images/c/c7/Calico_Critical_.png",
    },
    "Lady Geist": {
        "gloat": "https://deadlock.wiki/images/0/0c/Lady_Geist_Gloat.png",
        "critical": "https://deadlock.wiki/images/1/1e/Lady_Geist_Critical_.png",
    },
    "Viscous": {
        "gloat": "https://deadlock.wiki/images/6/64/Viscous_Gloat.png",
        "critical": "https://deadlock.wiki/images/e/ef/Viscous_Critical_.png",
    },
    "Grey Talon": {
        "gloat": "https://deadlock.wiki/images/1/11/Grey_Talon_Gloat.png",
        "critical": "https://deadlock.wiki/images/7/79/Grey_Talon_Critical.png",
    },
    "Lash": {
        "gloat": "https://deadlock.wiki/images/7/72/Lash_Gloat.png",
        "critical": "https://deadlock.wiki/images/b/b8/Lash_Critical.png",
    },
    "Paradox": {
        "gloat": "https://deadlock.wiki/images/e/e7/Paradox_Gloat.png",
        "critical": "https://deadlock.wiki/images/6/68/Paradox_Critical.png",
    },
    "Pocket": {
        "gloat": "https://deadlock.wiki/images/d/d4/Pocket_Gloat.png",
        "critical": "https://deadlock.wiki/images/e/e3/Pocket_Critical_.png",
    },
    "Rem": {
        "gloat": "https://deadlock.wiki/images/2/2f/Rem_Gloat_%28Familiar%29.png",
        "critical": "https://deadlock.wiki/images/5/54/Rem_Critical_%28Familar%29.png",
    },
}


HEROES_PER_ROW = 6


def total_games(g):
    return g["wins"] + g["losses"]


def win_rate(g):
    games = total_games(g)
    return (g["wins"] / games * 100) if games else 0


def hero_image(hero, stats):
    mood = "gloat" if win_rate(stats) >= 50 else "critical"
    return HERO_IMAGES[hero][mood]


def hero_table(heroes):
    """Build a single markdown table for a chunk of heroes (<= HEROES_PER_ROW)."""
    headers = []
    images = []
    results = []

    for hero in heroes:
        hero_stats = data.get(hero, {"wins": 0, "losses": 0})

        headers.append(hero)
        images.append(f'<img src="{hero_image(hero, hero_stats)}" width="60">')
        results.append(
            f'{hero_stats["wins"]}W - '
            f'{hero_stats["losses"]}L '
            f'({win_rate(hero_stats):.1f}%)'
        )

    return (
        "| " + " | ".join(headers) + " |\n"
        "|" + "|".join([":---:"] * len(headers)) + "|\n"
        "| " + " | ".join(images) + " |\n"
        "| " + " | ".join(results) + " |"
    )


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

    # Most-played heroes first; ties keep GAME_HEROES order (stable sort).
    heroes_sorted = sorted(
        GAME_HEROES[name],
        key=lambda h: total_games(data.get(h, {"wins": 0, "losses": 0})),
        reverse=True,
    )

    # Split into chunks of HEROES_PER_ROW, stacking one table per chunk
    # going down the page rather than one huge wide row.
    tables = [
        hero_table(heroes_sorted[i : i + HEROES_PER_ROW])
        for i in range(0, len(heroes_sorted), HEROES_PER_ROW)
    ]

    return (
        f"{heading_html}\n\n"
        f"{stats_html}\n\n"
        f"<h4 align=\"center\">Heroes</h4>\n\n"
        + "\n\n".join(tables)
    )


sections = [
    game_section("Deadlock", data["Deadlock"]),
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
