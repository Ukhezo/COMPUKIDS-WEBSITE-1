"""
build.py - Generates pages from the JSON files in data/.

- data/heroes.json    -> avenger-1.html ... avenger-6.html
- data/languages.json -> languages.html

Each page's details live in one place. Running this script rebuilds the
pages so they all use the same layout. To change a hero or a language,
edit the JSON and run the script again.

Usage (from the project root):
    python tools/build.py
"""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "heroes.json"
LANGUAGES_FILE = ROOT / "data" / "languages.json"

MENU = """    <nav id="menu" aria-label="Main menu">
      <a href="index.html">Home</a>
      <a href="about.html">About Us</a>
      <a href="languages.html">Languages</a>
      <a href="contact.html">Contact</a>
      <a href="links.html">Links</a>
    </nav>"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="CompuKids is an app development company based in Durban, South Africa. Meet the Avengers and find out about us.">
    <title>{name} | UKHEZO-COMPUKIDS</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
{menu}
    <h2>{name}</h2>
    <div class="gallery single">
      <img src="images/{image}" alt="{name}">
    </div>
    <h4>Bio</h4>
{bio}
    <h4>Power Stats</h4>
{stats}
  </body>
</html>
"""

BIO_FIELDS = [
    ("Full name", "full_name"),
    ("Place of birth", "place_of_birth"),
    ("Alignment", "alignment"),
    ("Gender", "gender"),
    ("Race", "race"),
]


def line(label, value):
    """Return one '<p><b>Label:</b> value</p>' line, indented to match the page."""
    return f"    <p><b>{escape(label)}:</b> {escape(str(value))}</p>"


def validate(hero):
    """Stop with a clear message if a hero entry is missing data or has a bad stat."""
    required = ["id", "name", "image", "power_stats"] + [key for _, key in BIO_FIELDS]
    missing = [key for key in required if key not in hero]
    if missing:
        raise ValueError(f"Hero {hero.get('name', '?')} is missing: {', '.join(missing)}")

    for stat, value in hero["power_stats"].items():
        if not isinstance(value, int) or not 0 <= value <= 100:
            raise ValueError(f"{hero['name']}: {stat} must be a whole number from 0 to 100")

    if not (ROOT / "images" / hero["image"]).exists():
        raise FileNotFoundError(f"{hero['name']}: image images/{hero['image']} not found")


def build_page(hero):
    """Create the full HTML for one hero."""
    bio = "\n".join(line(label, hero[key]) for label, key in BIO_FIELDS)
    stats = "\n".join(line(stat, f"{value}%") for stat, value in hero["power_stats"].items())
    return PAGE_TEMPLATE.format(
        menu=MENU,
        name=escape(hero["name"]),
        image=escape(hero["image"]),
        bio=bio,
        stats=stats,
    )


LANGUAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="The programming languages CompuKids uses to build websites, mobile apps, data tools and games.">
    <title>Programming Languages | UKHEZO-COMPUKIDS</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
{menu}
    <h2>Programming Languages</h2>
    <p class="intro">We pick the right language for each job. Here are the {count} languages our team
      uses to build websites, mobile apps, data tools and games. Open a card to see real code.</p>
    <div class="filters" role="group" aria-label="Filter languages by type">
      <button type="button" class="filter active" data-filter="all" aria-pressed="true">All</button>
{filters}
    </div>
    <p id="lang-count" class="lang-count" aria-live="polite">Showing {count} languages</p>
    <div class="lang-grid">
{cards}
    </div>
    <script src="script.js"></script>
  </body>
</html>
"""

CARD_TEMPLATE = """      <article class="lang-card" id="{id}" data-category="{category}">
        <div class="lang-head" style="background: {color}; color: {text_color};">
          <span class="lang-badge">{short}</span>
          <div>
            <h3>{name}</h3>
            <span class="lang-meta">{category} &middot; since {year}</span>
          </div>
        </div>
        <div class="lang-body">
          <p class="lang-tagline">{tagline}</p>
          <p><b>We use it for:</b> {we_use_it_for}</p>
          <p><b>Built with {name}:</b> {built_with_it}</p>
          <p><b>Level:</b> <span class="level">{level}</span></p>
          <details>
            <summary>Show code <span class="file">{file}</span></summary>
            <pre><code>{code}</code></pre>
          </details>
          <a class="learn" href="{docs}" target="_blank" rel="noopener">Learn {name} &rarr;</a>
        </div>
      </article>"""

LANGUAGE_FIELDS = ["id", "name", "category", "color", "text_color", "year", "level", "tagline",
                   "we_use_it_for", "built_with_it", "docs", "file", "code"]
SHORT_NAMES = {"javascript": "JS", "typescript": "TS", "python": "Py", "sql": "SQL", "kotlin": "Kt",
               "java": "Java", "swift": "Swift", "dart": "Dart", "csharp": "C#", "cpp": "C++"}


def validate_language(lang):
    """Stop with a clear message if a language entry is missing data."""
    missing = [key for key in LANGUAGE_FIELDS if key not in lang]
    if missing:
        raise ValueError(f"Language {lang.get('name', '?')} is missing: {', '.join(missing)}")
    if not lang["docs"].startswith("https://"):
        raise ValueError(f"{lang['name']}: docs link must start with https://")
    if not isinstance(lang["year"], int):
        raise ValueError(f"{lang['name']}: year must be a whole number")


def build_languages_page(languages):
    """Create languages.html with one card per language and a filter button per category."""
    categories = sorted({lang["category"] for lang in languages})
    filters = "\n".join(
        f'      <button type="button" class="filter" data-filter="{escape(c)}" aria-pressed="false">{escape(c)}</button>'
        for c in categories
    )
    cards = "\n".join(
        CARD_TEMPLATE.format(
            id=escape(lang["id"]),
            name=escape(lang["name"]),
            short=escape(SHORT_NAMES.get(lang["id"], lang["name"][:2])),
            category=escape(lang["category"]),
            color=escape(lang["color"]),
            text_color=escape(lang["text_color"]),
            year=lang["year"],
            level=escape(lang["level"]),
            tagline=escape(lang["tagline"]),
            we_use_it_for=escape(lang["we_use_it_for"]),
            built_with_it=escape(", ".join(lang["built_with_it"])),
            docs=escape(lang["docs"]),
            file=escape(lang["file"]),
            code=escape(lang["code"]),
        )
        for lang in languages
    )
    return LANGUAGE_TEMPLATE.format(menu=MENU, count=len(languages), filters=filters, cards=cards)


def main():
    heroes = json.loads(DATA_FILE.read_text(encoding="utf-8"))["heroes"]

    for hero in heroes:
        validate(hero)
        output = ROOT / f"avenger-{hero['id']}.html"
        output.write_text(build_page(hero), encoding="utf-8")
        print(f"Built {output.name} ({hero['name']})")

    print(f"Done: {len(heroes)} hero pages generated.")

    languages = json.loads(LANGUAGES_FILE.read_text(encoding="utf-8"))["languages"]
    for lang in languages:
        validate_language(lang)
    (ROOT / "languages.html").write_text(build_languages_page(languages), encoding="utf-8")
    print(f"Built languages.html ({len(languages)} languages)")


if __name__ == "__main__":
    main()
