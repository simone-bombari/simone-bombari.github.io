# Simone Bombari's website

Live site: https://simone-bombari.github.io/

This is a plain HTML/CSS website. The layout is adapted with permission from
[Yijun Dong's website](https://github.com/dyjdongyijun/dyjdongyijun.github.io),
using its jemdoc styles. There is no Jekyll or jemdoc build step and no package
installation is required.

## Making changes

- `index.html`: biography, contact details, selected publications, education.
- `index_research.html`: all publications and preprints.
- `index_teach.html`: teaching and outreach.
- `cv/index.html`: CV page, education, visits, and internships.
- `assets/pdf/CV.pdf`: the downloadable CV; replace this file to update it.
- `assets/img/smile_2_square.jpg`: the profile photo.
- `jemdoc.css`: the appearance and small mobile/accessibility adjustments.

Edit the HTML directly. When adding a selected paper, update both the homepage
and the Research page. `_bibliography/papers.bib` is retained as a downloadable
bibliography; it does not generate the publication lists.

## Preview and validate

Using an existing Python 3.9 or newer installation:

```sh
python3 scripts/prepare_site.py
python3 -m http.server 8000 --directory _site --bind 127.0.0.1
```

Visit http://127.0.0.1:8000/ and press Ctrl+C to stop the server.
The preparation script validates local links, image alternative text, the CV,
and sitemap, then copies only the public website files into `_site`.

## Publishing

Commit your edits and push to `master`. The `Deploy site` GitHub Actions workflow
validates and publishes `_site` to `gh-pages`. Pull requests validate without
publishing. GitHub Pages should retain **Deploy from a branch → gh-pages → /(root)**
in the repository's Settings → Pages. `.nojekyll` prevents a Jekyll rebuild.

The old `/publications/`, `/teaching/`, and `/projects/` URLs redirect to their
new pages. `/cv/` and `/assets/pdf/CV.pdf` continue to work.

The earlier al-folio/Jekyll source files remain in the repository for reference;
they are not deployed and changes to them do not change the HTML site.
