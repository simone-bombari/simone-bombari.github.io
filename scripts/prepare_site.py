"""Validate and stage the plain HTML website using only the Python standard library."""

from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "_site"
# Publish only the website. Legacy Jekyll code and example assets stay in the repo.
FILES = {
    "index.html": "index.html",
    "index_research.html": "index_research.html",
    "index_teach.html": "index_teach.html",
    "404.html": "404.html",
    "jemdoc.css": "jemdoc.css",
    ".nojekyll": ".nojekyll",
    "robots.txt": "robots.txt",
    "sitemap.xml": "sitemap.xml",
    "publications/index.html": "publications/index.html",
    "teaching/index.html": "teaching/index.html",
    "projects/index.html": "projects/index.html",
    "cv/index.html": "cv/index.html",
    "assets/img/smile_2_square.jpg": "assets/img/smile_2_square.jpg",
    "assets/pdf/CV.pdf": "assets/pdf/CV.pdf",
    "_bibliography/papers.bib": "assets/bibliography/papers.bib",
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
    print(f"Validated {len(pages)} HTML pages and their local links; staged {len(FILES)} files in _site.")


if __name__ == "__main__":
    prepare()
