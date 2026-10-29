# Editing the website

The site is built with [Quarto](https://quarto.org) and published by Netlify
every time something is pushed to `master`. Every file below can be edited
directly on GitHub (pencil icon) or locally in RStudio.

## Where things live

| To change…                    | Edit                                           |
|-------------------------------|------------------------------------------------|
| Home page / About me / Contact | `index.qmd`                                   |
| Research                      | `research.qmd`                                 |
| Publications                  | `publications.yml`                             |
| Science outreach              | `outreach.qmd`                                 |
| Illustrations                 | `illustrations.yml` + `images/illustrations/`  |
| CV                            | replace `media/CV.pdf` (same name)             |
| Menu, footer links, site name | `_quarto.yml`                                  |
| Colours and fonts             | `styles/theme.scss` (dark mode: `styles/dark.scss`) |
| Photos and figures            | `images/`                                      |

`README.md` is your GitHub profile page, not part of the website.

## Add a publication

**Option 1 — from the DOI, on GitHub (no computer setup needed)**
1. Open the repository on GitHub → **Actions** → **Add publication** → **Run workflow**.
2. Paste the DOI (e.g. `10.1073/pnas.2524274123`) and press **Run workflow**.
3. A minute later the paper is in `publications.yml` and the site rebuilds.
   Open the file afterwards to check it (and add a `code:` or `note:` line if you like).

**Option 2 — from the DOI, on your computer**

```bash
python3 scripts/add_publication.py 10.1073/pnas.2524274123
```

**Option 3 — by hand.** Copy any entry in `publications.yml`, paste it at the
top and change the details. Only `title`, `authors`, `journal` and `year`
are required. The comment block at the top of the file explains every field.

Papers that are in press or under review: add `status: In press` (or
`Under review`) and leave out the DOI. They are listed at the top of the
Publications page. When the paper is out, delete that entry and add the
published version (option 1 or 2 will remind you).

## Add an illustration

1. Upload the image to `images/illustrations/` (any size; jpg or png).
   On GitHub: open the folder → **Add file** → **Upload files**.
2. Add three lines at the top of `illustrations.yml`:

   ```yaml
   - file: my-drawing.png
     title: My drawing
     text: The story behind it (optional).
   ```

The build makes small web copies automatically, so full-resolution scans are fine.
The first six illustrations in the list also appear on the home page.

## Preview on your computer

Open `academic.Rproj` in RStudio and click **Render Website** in the Build pane,
or in a terminal:

```bash
quarto preview
```

RStudio already includes Quarto. Otherwise install it from
<https://quarto.org/docs/get-started/>. (For smaller preview images,
`pip install pillow`; on a Mac the built-in `sips` tool is used otherwise.)

## Contact form

Messages sent through the form on the home page arrive in Netlify under
**Forms → contact** (you can turn on email notifications there).

## Old site

The previous Hugo/Wowchemy version is in the git history. The old blog posts
are kept, unpublished, in `_archive/blog/`.
