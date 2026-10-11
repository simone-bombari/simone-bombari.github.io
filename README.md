# Simone Bombari's website

Live site: https://simone-bombari.github.io/

This is a plain HTML/CSS website. The layout is adapted with permission from
[Yijun Dong's website](https://github.com/dyjdongyijun/dyjdongyijun.github.io),
using its jemdoc styles. There is no Jekyll or jemdoc build step and no package
installation is required.

## Making changes

The five files for updating your information are all at the top level:

| File                  | What to update                                               |
| --------------------- | ------------------------------------------------------------ |
| `index.html`          | Biography, contact details, selected publications, education |
| `index_research.html` | All publications and preprints                               |
| `index_teach.html`    | Teaching and outreach                                        |
| `CV.pdf`              | Replace with your updated PDF, keeping the same filename     |
| `profile.jpg`         | Replace with your updated photo, keeping the same filename   |

Edit the HTML directly. When adding a selected paper, update both the homepage
and the Research page. CV links open the PDF directly in a new tab.
The links inside the HTML refer to the public website paths; keep those paths
when replacing the PDF or photo.

Everything else is organized under `support/`: styling, deployment helpers,
redirects, and the earlier theme files. You do not need to edit these for normal
content updates. Git and GitHub's hidden folders remain in place.

The contact address is plain text: `simone (dot) bombari [at] nyu (dot) edu`.
Keep it as text rather than an email link.

The "games" and "cooking" links in About Me open a random image from their
matching folders under `random_images/`, in a new tab. Add or remove images
in `random_images/games/` or `random_images/cooking/`, then commit and push.
The deployment automatically updates the choices. Keep at least one image in
each folder. JPG, JPEG, PNG, GIF, WebP, and AVIF files are supported.

An optional downloadable BibTeX copy lives at `support/bibliography/papers.bib`.
Update it only if you want that download to reflect bibliography changes;
it does not generate the publication lists.

## Preview and validate

Using an existing Python 3.9 or newer installation:

```sh
python3 support/prepare_site.py
python3 -m http.server 8000 --directory support/_site --bind 127.0.0.1
```

Visit http://127.0.0.1:8000/ and press Ctrl+C to stop the server.
The preparation script validates local links, image alternative text, the CV,
and sitemap, then copies only the public website files into `support/_site`.
This folder is generated; edit the five source files rather than its copies.

## Publishing

Commit your edits and push to `master`. The `Deploy site` GitHub Actions workflow
validates and publishes `support/_site` to `gh-pages`. Pull requests validate without
publishing. GitHub Pages should retain **Deploy from a branch → gh-pages → /(root)**
in the repository's Settings → Pages. `.nojekyll` prevents a Jekyll rebuild.

The old `/publications/`, `/teaching/`, and `/projects/` URLs redirect to their
new pages. `/cv/` redirects to the PDF; `/assets/pdf/CV.pdf` continues to work.

The earlier al-folio/Jekyll source files and unused assets are preserved in
`support/legacy/` for reference. They are not deployed.
