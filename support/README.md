# Supporting material

Normal content updates use the five files at the repository's top level.

- `prepare_site.py` validates those files and copies them to their public URL
  paths in `_site/`. It also copies images from `random_images/` and generates
  the two random image links using `random-images.js`. GitHub's deployment
  workflow runs this script.
- `jemdoc.css`, `404.html`, `.nojekyll`, `robots.txt`, and `sitemap.xml` support
  styling, hosting, and search engines.
- `redirects/` keeps older page links working.
- `bibliography/papers.bib` supplies the optional BibTeX download.
- `legacy/` preserves the old Jekyll theme, configuration, source content,
  unused assets, documentation, and existing local tools.
- `_site/` is generated preview/deployment output and is ignored by Git.

The source `CV.pdf` is copied to `/CV.pdf`, the compatible `/assets/pdf/CV.pdf`,
and a versioned PDF URL based on its contents. Published CV links and `/cv/`
use the versioned copy to avoid stale browser caches. The source `profile.jpg`
is copied to `/assets/img/smile_2_square.jpg`. There is no separate CV page to update.
