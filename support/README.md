# Supporting material

Normal content updates use the six files at the repository's top level.

- `prepare_site.py` validates those files and copies them to their public URL
  paths in `_site/`. GitHub's deployment workflow runs this script.
- `jemdoc.css`, `404.html`, `.nojekyll`, `robots.txt`, and `sitemap.xml` support
  styling, hosting, and search engines.
- `redirects/` keeps older page links working.
- `bibliography/papers.bib` supplies the optional BibTeX download.
- `legacy/` preserves the old Jekyll theme, configuration, source content,
  unused assets, documentation, and existing local tools.
- `_site/` is generated preview/deployment output and is ignored by Git.

The source files `CV.pdf`, `profile.jpg`, and `index_cv.html` are copied to the
existing public paths `/assets/pdf/CV.pdf`, `/assets/img/smile_2_square.jpg`,
and `/cv/index.html`. Their locations in this folder do not change the site's URLs.
