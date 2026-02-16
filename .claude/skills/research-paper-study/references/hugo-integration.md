# Hugo Blog Integration

Guide for generating Hugo blog posts from research paper study notes.

## Blog Structure

Hugo blog location: `/Users/gil-yoonhee/VSCodeProject/moripiri.github.io`

Hugo uses **page bundles**:
```
content/posts/<slug>/
├── index.md
└── images/
    ├── figure1-architecture.png
    ├── figure2-main-results.png
    └── ...
```

## Slug Generation

From paper title to URL-friendly slug:
- Lowercase all characters
- Replace spaces with hyphens
- Remove special characters (keep only a-z, 0-9, hyphens)
- Max length: ~60 characters

Examples:
- "Attention Is All You Need" → `attention-is-all-you-need`
- "BERT: Pre-training of Deep Bidirectional Transformers" → `bert-pretraining-deep-bidirectional-transformers`
- "Recursive Language Models" → `recursive-language-models`

## Frontmatter Format

Use this exact format (minimal, matching existing posts):

```yaml
---
title: "<Paper Title> 요약"  # Korean: "요약", English: "Summary"
date: <YYYY-MM-DD>
draft: true
tags: ["Paper Review", "<relevant-tag>"]
ShowToc: true
description: "<one-line paper description>"
---
```

**Tags suggestions by domain**:
- NLP: `"NLP"`, `"Transformers"`, `"LLM"`
- CV: `"Computer Vision"`, `"Image Processing"`
- RL: `"Reinforcement Learning"`
- General ML: `"Machine Learning"`, `"Deep Learning"`

## Content Structure

### CRITICAL: What to preserve

**Research-paper-study generates technical depth summaries. DO NOT simplify for blog.**

The blog should contain:
- Full complexity analysis (O(n²), memory bounds, etc.)
- Architectural details (layer counts, dimensions, hyperparameters)
- Complete experimental tables and ablations
- Cost/performance tradeoffs with concrete numbers
- Detailed insights sections

Only add the AI notice and convert image format. Everything else stays intact.

### Required elements

**1. AI Notice** (MUST be at top):
```markdown
> **🤖 AI Summary Notice**
> 이 글은 AI(Claude)가 논문을 읽고 작성한 요약입니다. 부정확한 내용이 있을 수 있으니, 정확한 정보는 원문을 참고해주세요.

<!--more-->
```

For English:
```markdown
> **🤖 AI Summary Notice**
> This post is a paper summary written by AI (Claude). It may contain inaccuracies — please refer to the original paper for precise details.

<!--more-->
```

**Important**: `<!--more-->` is the excerpt separator. Must appear after AI notice.

**2. Paper metadata**:
```markdown
**저자:** [Author names]  
**발행년도:** [Publication year]  
**링크:** [arXiv/DOI URL]
```

**3. Main content**:
**Use the research-paper-study generated summary AS-IS.**

DO NOT change the structure or simplify the content. Keep:
- Problem definition (with complexity/bottleneck analysis)
- Key contributions (architectural details, quantitative metrics)
- Methodology (equations, hyperparameters, design choices)
- Experimental results (tables, ablations, cost analysis)
- Computational complexity analysis
- Limitations and future directions
- Insights (paradigm shifts, engineering excellence, practical implications)
- References (with arXiv/DOI links)
- Tags

The technical depth is the main value - preserve it all.

## Image Handling

### Obsidian → Hugo conversion

**Obsidian wiki-link format**:
```markdown
![[attachments/papers/1706.03762-fig1.png]]
*Figure 1: Transformer architecture*
```

**Hugo format**:
```markdown
<p align="center"><img src="images/figure1-architecture.png" alt="Transformer Architecture"></p>

*Figure 1: Transformer architecture*
```

**Conversion steps**:
1. Extract image filename from wiki-link: `1706.03762-fig1.png`
2. Copy to `content/posts/<slug>/images/`
3. Optionally rename to descriptive name: `figure1-architecture.png`
4. Replace wiki-link with Hugo `<img>` tag
5. Keep caption as separate italicized line

### Image placement

Images should remain **inline** at their original positions:
- Architecture diagrams → within Methodology section
- Result plots → within Experimental Results section
- Comparison tables → where contextually appropriate

Do NOT move all images to end or create separate "Figures" section.

### Naming conventions

**Descriptive naming** (preferred):
```
figure1-architecture.png
figure2-attention-mechanism.png
figure3-main-results.png
figure4-ablation-study.png
```

**Or keep original** (simpler):
```
2512.24601-fig1.png
2512.24601-fig2.png
```

Both work, descriptive is better for readability.

## Workflow Example

**Input**: Study notes in markdown (Obsidian format)

**Output**: Hugo blog post

```bash
# 1. Create directory
mkdir -p content/posts/attention-is-all-you-need/images

# 2. Copy images
cp paper-images/1706.03762-fig*.png content/posts/attention-is-all-you-need/images/

# 3. Convert markdown
# - Replace wiki-links with <img> tags
# - Add frontmatter
# - Add AI notice + TL;DR
# - Add <!--more--> separator

# 4. Write to file
# content/posts/attention-is-all-you-need/index.md

# 5. Preview (optional)
cd /Users/gil-yoonhee/VSCodeProject/moripiri.github.io
hugo server -D
# Open http://localhost:1313/posts/attention-is-all-you-need/
```

## Publishing

**Draft → Published**:
1. Review the generated post
2. Verify images display correctly
3. Check for any inaccuracies
4. Update frontmatter: `draft: false`
5. Commit and push to GitHub

Hugo will automatically rebuild and deploy.

## Math Support

Hugo supports KaTeX for math rendering.

**Inline math**: `$E = mc^2$`  
**Display math**: `$$\text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$`

Keep math equations as-is from the study notes - they'll render correctly.

## Language-specific Notes

**Korean posts**:
- Title: `"<논문 제목> 요약"`
- AI notice in Korean
- Content in Korean (technical terms in English where conventional)

**English posts**:
- Title: `"<Paper Title> Summary"`
- AI notice in English
- Content in English

## Common Issues

**1. Images not displaying**:
- Check path is `images/filename.png` (relative to index.md)
- Verify file exists in page bundle
- Check filename matches exactly (case-sensitive)

**2. Math not rendering**:
- Ensure frontmatter doesn't disable math
- Check KaTeX delimiters: `$...$` or `$$...$$`

**3. Excerpt too long**:
- Move `<!--more-->` earlier
- Should be after TL;DR, before main content

**4. Draft not showing**:
- Use `hugo server -D` (with `-D` flag for drafts)
- Check `draft: true` in frontmatter
