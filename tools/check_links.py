"""
check_links.py - Checks every HTML page for broken links and missing images.

It reads each .html file in the project, finds every href and src that
points to a local file, and reports any that do not exist. Web links
(http, https, mailto, tel) and page anchors (#) are skipped.

Usage (from the project root):
    python tools/check_links.py

Exit code is 0 when everything is fine and 1 when something is broken,
so the script can also be used in automated checks.
"""

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "javascript"}


class LinkCollector(HTMLParser):
    """Collects the href and src values from an HTML page."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.links.append((tag, value))


def is_local(link):
    """True if the link points to a file in this project."""
    parsed = urlparse(link)
    return parsed.scheme not in SKIP_SCHEMES and not link.startswith("#")


def check_page(page):
    """Return a list of broken links found in one page."""
    collector = LinkCollector()
    collector.feed(page.read_text(encoding="utf-8"))

    broken = []
    for tag, link in collector.links:
        if not is_local(link):
            continue
        target = (page.parent / urlparse(link).path).resolve()
        if not target.exists():
            broken.append((tag, link))
    return broken


def main():
    pages = sorted(ROOT.glob("*.html"))
    total_broken = 0

    for page in pages:
        broken = check_page(page)
        total_broken += len(broken)
        for tag, link in broken:
            print(f"BROKEN  {page.name}: <{tag}> -> {link}")

    if total_broken:
        print(f"\n{total_broken} broken link(s) found in {len(pages)} pages.")
        sys.exit(1)

    print(f"All links OK: checked {len(pages)} pages.")


if __name__ == "__main__":
    main()
