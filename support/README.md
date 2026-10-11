# Supporting material

Normal content updates use the five files at the repository's top level.

- `prepare_site.py` validates those files and copies them to their public URL
  paths in `_site/`. It also copies images from `random_images/` and generates
  the two random image links. GitHub's deployment workflow runs this script.
- `jemdoc.css`, `404.html`, `.nojekyll`, `robots.txt`, and `sitemap.xml` support
  styling, hosting, and search engines.
- `redirects/` keeps older page links working.
- `bibliography/papers.bib` supplies the optional BibTeX download.
- `legacy/` preserves the old Jekyll theme, configuration, source content,
  unused assets, documentation, and existing local tools.
- `_site/` is generated preview/deployment output and is ignored by Git.

The source files `CV.pdf` and `profile.jpg` are copied to the existing public
paths `/assets/pdf/CV.pdf` and `/assets/img/smile_2_square.jpg`. The previous
`/cv/` page redirects to the PDF. There is no separate CV page to update.
