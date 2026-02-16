# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hugo static site blog using the PaperMod theme (git submodule). Deployed to GitHub Pages at https://moripiri.github.io/. Content is primarily in Korean.

## Commands

- **Dev server**: `hugo server`
- **Build**: `hugo --gc --minify`
- **Create new post**: `hugo new posts/<post-name>/index.md` (uses `archetypes/post.md` template)

Hugo version 0.146.0+ required (CI uses 0.147.2 extended with Dart Sass).

## Architecture

- **hugo.yaml** — Main site configuration (theme settings, menus, social icons, search, analytics)
- **content/posts/** — Blog posts as page bundles (each post in its own directory with `index.md` + images)
- **layouts/partials/** — Custom template overrides on top of PaperMod:
  - `head.html` — Adds KaTeX math rendering via CDN
  - `header.html` — Custom theme toggle (auto/light/dark with localStorage)
  - `helpers/katex.html` — KaTeX auto-render configuration with `$$`, `$`, `\[\]`, `\(\)` delimiters
- **themes/PaperMod/** — Git submodule, do not edit directly
- **static/** — Favicons and Google site verification
- **public/** — Generated output, do not edit (rebuilt on deploy)

## Deployment

GitHub Actions (`.github/workflows/hugo.yaml`) auto-deploys on push to `master`. The workflow installs Hugo + Dart Sass, builds with `--gc --minify`, and deploys to GitHub Pages.

## Post Frontmatter

Posts use `archetypes/post.md` as template. Key fields: `title`, `date`, `tags`, `author: "mori"`, `math: true` (for KaTeX), `showToc`, `draft`. The `editPost.URL` points to the GitHub issues page.

## Key Integrations

- **KaTeX**: Math rendering enabled per-post with `math: true` in frontmatter
- **Fuse.js**: Client-side search at `/search/`
- **Google Analytics**: GA ID configured in hugo.yaml
