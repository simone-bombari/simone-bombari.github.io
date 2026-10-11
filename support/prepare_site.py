"""Validate and stage the plain HTML website using only the Python standard library."""

from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "support" / "_site"
# Source locations are kept simple; published URLs stay the same after cleanup.
FILES = {
    "index.html": "index.html",
    "index_research.html": "index_research.html",
    "index_teach.html": "index_teach.html",
    "index_cv.html": "cv/index.html",
    "profile.jpg": "assets/img/smile_2_square.jpg",
    "CV.pdf": "assets/pdf/CV.pdf",
    "support/404.html": "404.html",
    "support/jemdoc.css": "jemdoc.css",
    "support/.nojekyll": ".nojekyll",
    "support/robots.txt": "robots.txt",
    "support/sitemap.xml": "sitemap.xml",
    "support/redirects/publications/index.html": "publications/index.html",
    "support/redirects/teaching/index.html": "teaching/index.html",
    "support/redirects/projects/index.html": "projects/index.html",
    "support/bibliography/papers.bib": "assets/bibliography/papers.bib",
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.ids = set()

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        for key in ("href", "src"):
            if attributes.get(key):
                self.references.append(attributes[key])
        if tag == "img" and not attributes.get("alt"):
            raise ValueError("Every image needs alternative text")
        if tag == "meta" and attributes.get("http-equiv", "").lower() == "refresh":
            self.references.append(attributes["content"].split("url=", 1)[1].strip())


def prepare():
    for source in FILES:
        if not (ROOT / source).is_file():
            raise FileNotFoundError(source)
    # Refuse a symlink so cleaning generated output cannot affect another folder.
    if OUTPUT.is_symlink():
        raise ValueError("_site must not be a symlink")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    for source, destination in FILES.items():
        target = OUTPUT / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, target)

    pages = {}
    for path in OUTPUT.rglob("*.html"):
        page = Page()
        page.feed(path.read_text())
        pages[path.resolve()] = page

    for path, page in pages.items():
        for reference in page.references:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            if not url.path:
                target = path
            elif url.path.startswith("/"):
                target = OUTPUT / unquote(url.path.lstrip("/"))
            else:
                target = path.parent / unquote(url.path)
            target = target.resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.is_relative_to(OUTPUT.resolve()) or not target.is_file():
                raise ValueError(f"Broken local link in {path.relative_to(OUTPUT)}: {reference}")
            if url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                raise ValueError(f"Missing anchor in {path.relative_to(OUTPUT)}: {reference}")
    ET.parse(OUTPUT / "sitemap.xml")
    if not (OUTPUT / "assets/pdf/CV.pdf").read_bytes().startswith(b"%PDF-"):
        raise ValueError("CV.pdf is not a PDF")
    print(f"Validated {len(pages)} HTML pages and their local links; staged {len(FILES)} files in support/_site.")


if __name__ == "__main__":
    prepare()
