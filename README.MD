### Deploying to GitHub Pages with MkDocs

To publish your MkDocs site to GitHub Pages, run:

    mkdocs gh-deploy

This command will:
- Build the static site from your docs/ directory
- Create or update the gh-pages branch
- Push the generated site to GitHub

After deployment, ensure GitHub Pages is configured to use the gh-pages branch (Settings → Pages).

For local preview before deploying:

    mkdocs serve
