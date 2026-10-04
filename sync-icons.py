"""Copy icons.svg into every page of the web v2 prototype that has an icon block.

Browsers refuse <use href="icons.svg#id"> on pages opened from disk, so each page carries the
sprite inline between <!-- icons:start --> and <!-- icons:end -->. Edit icons.svg, then run:

    python3 ui-desgn/web/v2/sync-icons.py
"""

from pathlib import Path
import re

HERE = Path(__file__).parent
START, END = "<!-- icons:start -->", "<!-- icons:end -->"
BLOCK = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)


def main() -> None:
    sprite = (HERE / "icons.svg").read_text().strip()
    block = f"{START}\n{sprite}\n{END}"
    for page in sorted(HERE.glob("*.html")):
        html = page.read_text()
        if START not in html:
            print(f"skipped {page.name}, it has no icon block")
            continue
        page.write_text(BLOCK.sub(lambda _: block, html, count=1))
        print(f"synced {page.name}")


if __name__ == "__main__":
    main()
