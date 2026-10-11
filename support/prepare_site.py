"""Validate and stage the plain HTML website using only the Python standard library."""

from html.parser import HTMLParser
from pathlib import Path
import json
import shutil
from urllib.parse import quote, unquote, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "support" / "_site"
# Source locations are kept simple; published URLs stay the same after cleanup.
FILES = {
    "index.html": "index.html",
    "index_research.html": "index_research.html",
    "index_teach.html": "index_teach.html",
    "support/redirects/cv/index.html": "cv/index.html",
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
    files = FILES.copy()
    image_choices = {}
    for category in ("games", "cooking"):
        folder = ROOT / "random_images" / category
        images = sorted(
            path for path in folder.rglob("*")
            if path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}
        )
        if not images:
            raise ValueError(f"Add at least one image to random_images/{category}/")
        image_choices[category] = []
        for image in images:
            relative = image.relative_to(ROOT).as_posix()
            files[relative] = relative
            image_choices[category].append("/" + quote(relative, safe="/"))

    for source in files:
        if not (ROOT / source).is_file():
            raise FileNotFoundError(source)
    # Refuse a symlink so cleaning generated output cannot affect another folder.
    if OUTPUT.is_symlink():
        raise ValueError("_site must not be a symlink")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    for source, destination in files.items():
        target = OUTPUT / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, target)

    # Static hosting cannot list folders in the browser. Generate the image choices
    # during deployment so adding/removing photos never requires editing the HTML.
    for category, images in image_choices.items():
        target = OUTPUT / "random_images" / category / "index.html"
        target.write_text(f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex">
    <title>{category.title()} | Simone Bombari</title>
  </head>
  <body>
    <p><a href="{images[0]}">Open a {category} image</a>.</p>
    <script>
      const images = {json.dumps(images)};
      window.location.replace(images[Math.floor(Math.random() * images.length)]);
    </script>
  </body>
</html>
''')

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
    total_files = len(files) + len(image_choices)
    print(f"Validated {len(pages)} HTML pages and their local links; staged {total_files} files in support/_site.")
    for category, images in image_choices.items():
        print(f"Random {category} link: {len(images)} images available.")


if __name__ == "__main__":
    prepare()
