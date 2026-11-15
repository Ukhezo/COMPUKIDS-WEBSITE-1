"""
build.py - Generates the Avenger hero pages from data/heroes.json.

Each hero's details live in one place (data/heroes.json). Running this
script rebuilds avenger-1.html ... avenger-6.html so every page uses the
same layout. To change a hero, edit the JSON and run the script again.

Usage (from the project root):
    python tools/build.py
"""

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "heroes.json"

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
    <div id="menu">
      <a href="index.html">Home</a>
      <a href="about.html">About Us</a>
      <a href="contact.html">Contact</a>
      <a href="links.html">Links</a>
    </div>
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
        name=escape(hero["name"]),
        image=escape(hero["image"]),
        bio=bio,
        stats=stats,
    )


def main():
    heroes = json.loads(DATA_FILE.read_text(encoding="utf-8"))["heroes"]

    for hero in heroes:
        validate(hero)
        output = ROOT / f"avenger-{hero['id']}.html"
        output.write_text(build_page(hero), encoding="utf-8")
        print(f"Built {output.name} ({hero['name']})")

    print(f"Done: {len(heroes)} hero pages generated.")


if __name__ == "__main__":
    main()
