---
name: summarize-paper
description: Summarizes an ML paper (PDF path or arXiv URL) and generates a Hugo blog post. Usage: /summarize-paper <pdf-path-or-arxiv-url> [ko|en]
---

You are generating a Hugo blog post that summarizes a machine learning paper.

## Step 1: Parse Input

The user provides an argument which is either:
- A **local PDF file path** (e.g., `/path/to/paper.pdf`)
- An **arXiv URL** (e.g., `https://arxiv.org/abs/2301.00001` or `https://arxiv.org/pdf/2301.00001`)

The user may also specify a language: `ko` for Korean (default) or `en` for English.

If no language is specified in the argument, ask the user:
- **Korean (ko)** — 한국어로 요약 (Recommended)
- **English (en)** — Summarize in English

## Step 2: Read the Paper

- **For a PDF file path**: Use the Read tool to read the PDF. For large PDFs, read in chunks using the `pages` parameter (e.g., pages "1-20", then "21-40", etc.).
- **For an arXiv URL**:
  1. Use WebFetch to fetch the abstract page (`https://arxiv.org/abs/XXXX.XXXXX`) to get the title, authors, and abstract.
  2. Use the Read tool to read the PDF if the user provides a local path, or ask the user to download the PDF if only a URL is given and the PDF cannot be fetched directly.

Read the full paper carefully. Pay attention to:
- Title, authors, date, venue
- Abstract and introduction (motivation/problem)
- Method/approach section (core contribution)
- Experiments and results
- Limitations and conclusion

## Step 2.5: Extract Figures

After reading the paper, download key figures to include in the blog post.

### For arXiv papers

1. Derive the ar5iv HTML URL from the arXiv ID: `https://ar5iv.labs.arxiv.org/html/XXXX.XXXXX`
2. Use `WebFetch` to fetch this HTML page. Identify figure `<img>` tags — look for figures with captions (e.g., architecture diagrams, main result plots, comparison tables rendered as images).
3. Select the **3-5 most important figures** (prioritize: architecture/method diagram, main results figure, key ablation/comparison plot).
4. Create the images directory: `content/posts/<slug>/images/`
5. Download each figure using Bash `curl -L -o content/posts/<slug>/images/<filename> <image-url>`. Name files descriptively:
   - `figure1-architecture.png`
   - `figure2-main-results.png`
   - `figure3-comparison.png`
   - etc.
6. If ar5iv is unavailable or figures cannot be extracted, note this and continue without images.

### For local PDFs (arXiv papers)

Since the user typically provides local PDFs of arXiv papers, extract figures via the ar5iv HTML version:
1. Ask the user for the arXiv ID if not already known (check the PDF metadata, filename, or content for clues like `arXiv:XXXX.XXXXX`).
2. Once the arXiv ID is known, follow the same ar5iv approach as above: fetch `https://ar5iv.labs.arxiv.org/html/XXXX.XXXXX`, identify key figures, and download them.
3. If the arXiv ID cannot be determined, search the web using the paper title to find the arXiv page, then proceed with the ar5iv approach.
4. If ar5iv is unavailable as a last resort, tell the user which figures would be valuable and ask them to export manually.

## Step 3: Generate the Blog Post

Create a Hugo page bundle at `content/posts/<slugified-title>/index.md`.

The slug should be derived from the paper title: lowercase, hyphens for spaces, ASCII only, max ~60 chars. For example: "Attention Is All You Need" → `attention-is-all-you-need`.

### Frontmatter

Use this exact frontmatter structure (matching the blog's existing conventions):

```yaml
---
title: "<Paper Title> 요약"  # or "<Paper Title> Summary" for English
date: <YYYY-MM-DD>T00:00:00+00:00  # today's date
tags: ["Paper Review", "<relevant-topic-tag>"]
author: "mori"
showToc: true
TocOpen: false
draft: true
hidemeta: false
comments: false
description: "<one-line description of the paper in chosen language>"
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true
UseHugoToc: true
math: true
editPost:
    URL: "https://github.com/moripiri/moripiri.github.io/issues"
    Text: "Suggest Changes"
    appendFilePath: true
---
```

### Content Structure

Write the post body in the chosen language (Korean or English) with these sections:

```
> **🤖 AI Summary Notice**
> 이 글은 AI(Claude)가 논문을 읽고 작성한 요약입니다. 부정확한 내용이 있을 수 있으니, 정확한 정보는 원문을 참고해주세요.

(For English posts, use instead:)
> **🤖 AI Summary Notice**
> This post is a paper summary written by AI (Claude). It may contain inaccuracies — please refer to the original paper for precise details.

## TL;DR
<2-3 sentence summary of the paper's key contribution>

<!--more-->

## Background / Motivation
<What problem does this paper address? Why is it important? What prior work existed?>

## Method
<Core approach and architecture. Use KaTeX math where appropriate:>
<- Inline math with `$...$`>
<- Display math with `$$...$$`>
<Include key equations from the paper. Explain them clearly.>
<Insert architecture/method diagram here if available:>
<p align="center"><img src="images/figure1-architecture.png" alt="description"></p>
<*caption describing the figure*>

## Key Results
<Main experimental findings. Mention datasets, baselines, and metrics.>
<Use bullet points or tables for clarity.>
<Insert main results figure/plot here if available:>
<p align="center"><img src="images/figure2-main-results.png" alt="description"></p>
<*caption describing the figure*>

## Limitations & Discussion
<What are the caveats? What does the paper not address? Future work directions.>

## Citation
<BibTeX entry or formatted citation>
```

### Writing Guidelines

- Be accurate to the paper. Do not hallucinate results or claims.
- For Korean posts: Use a natural Korean academic writing style. Technical terms can remain in English where conventional (e.g., Transformer, attention, gradient).
- Include all important equations using KaTeX syntax (`$...$` for inline, `$$...$$` for display).
- Keep the summary informative but concise — aim for a 5-10 minute read.
- Use `<!--more-->` after the TL;DR section as the excerpt separator.
- Embed figures using `<p align="center"><img src="images/filename.png" alt="description"></p>` followed by an italicized caption. Place them in contextually appropriate sections (architecture diagram in Method, result plots in Key Results, etc.).

## Step 4: Post-Generation

After creating the post file:

1. Use the Write tool to save the generated `index.md`.
2. Run `hugo server -D` (with drafts enabled) in the background using Bash.
3. Tell the user:
   - The post was created at `content/posts/<slug>/index.md`
   - Local preview is available at `http://localhost:1313/posts/<slug>/`
   - The post is currently a **draft** — set `draft: false` when ready to publish
   - They should review the summary for accuracy before publishing
   - **Figures**: List which figures were downloaded (or which ones the user should provide for local PDFs). Suggest they verify image quality and relevance in the preview.
