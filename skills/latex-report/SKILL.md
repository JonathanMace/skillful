---
name: latex-report
description: >-
  Produce a polished LaTeX report or PDF writeup using the right template,
  modern typography, and a dedicated report directory with a checked-in
  compiled PDF.  Use when asked to create, revise, or format a LaTeX report,
  conference draft, paper draft, or PDF writeup that should be authored in
  LaTeX.
license: MIT
---

# Producing Reports in LaTeX

This skill covers one-off LaTeX reports and PDF writeups: creating the source tree, choosing an appropriate document class, compiling with `pdflatex`, and checking in the resulting PDF alongside the source.

Use this skill when the user specifically wants a LaTeX deliverable or asks for a PDF writeup that should be authored in LaTeX rather than plain Markdown.

## Procedure: Producing a LaTeX Report

1. **Inspect the environment and report target first** — confirm that `pdflatex` is installed before creating or editing the report. If it is missing, stop and state clearly that LaTeX/PDF generation is blocked until `pdflatex` is available. Also inspect whether the user named a venue, format, existing report directory, or existing build instructions so you can follow the correct template instead of inventing one.
2. **Create or reuse a dedicated report directory** — keep each LaTeX report in its own subdirectory. Do not place the source files for multiple reports in the same directory. A report directory should contain that report's `.tex`, bibliography, figures, and compiled PDF.
3. **Choose the document style based on the target** — if the report is a conference draft, look up and follow the venue's official formatting guidance first. For ACM conference drafts, the common default is the ACM conference template in two-column form (for example, `acmart` with the conference layout). For a regular writeup with no venue constraints, default to a one-column `article` layout with 1-inch margins.
4. **Prefer modern typography over built-in defaults** — use a modern font family such as Libertine instead of the built-in Computer Modern defaults when the toolchain supports it. If the document uses math heavily, choose a matching modern math setup rather than mixing a modern text font with obviously mismatched math output.
5. **Lay out the source tree clearly** — keep the main entry point obvious (for example, `main.tex`), place figures in a `figures/` subdirectory, and keep local assets inside the report directory. Avoid dumping generated artifacts, unrelated notes, or another report's files into the same folder.
6. **Compile the report with `pdflatex`** — run `pdflatex` enough times for references, table of contents entries, and citations to settle. If the document includes a bibliography, run the appropriate bibliography tool (`bibtex` or `biber`, depending on the document) between `pdflatex` passes. Treat compilation warnings, missing assets, and unresolved references as issues to fix rather than ignoring them.
7. **Commit the PDF together with source updates** — whenever you change the LaTeX source for a report, update and commit the compiled PDF in the same change. The checked-in PDF is part of the deliverable, not an optional local artifact.

## Prerequisites and Blocking Conditions

- `pdflatex` must be installed and available on `PATH`
- Conference drafts need the venue's official author instructions if the user named a conference
- If required packages or templates are missing, surface that explicitly instead of silently falling back to a different layout

If the environment cannot compile LaTeX, do not pretend the PDF was produced successfully.

## When to Use LaTeX (vs Other Formats)

- Use LaTeX when the user explicitly asks for a LaTeX report, paper draft, conference draft, or PDF writeup that should be produced from LaTeX source
- Use LaTeX when the deliverable needs venue-specific academic formatting, citation-heavy structure, or a polished typeset PDF
- Do not force LaTeX when the user only wants a quick note, README update, or plain Markdown document
- If the requested deliverable is ambiguous, prefer the format the user named explicitly

## Default Style Rules

### Conference drafts

- Prefer the conference's published formatting rules over generic defaults
- For ACM conference drafts, the usual default is the ACM conference template with a two-column layout
- Do not switch a conference draft to `article` just because it is simpler if the venue expects something else

### General writeups

- Default to `article`
- Use 1-inch margins
- Use one-column layout unless the user or venue requires otherwise
- Keep the preamble lean; do not add unnecessary packages just because they are common in old templates

### Typography

- Prefer a modern font family such as Libertine over built-in defaults
- Keep typography consistent across the document
- If you introduce a modern text font, make sure headings, body text, and any math look intentional together

## Recommended Directory Layout

```
reports/
└── quarterly-review/
    ├── main.tex
    ├── references.bib
    ├── figures/
    │   └── architecture.pdf
    └── main.pdf
```

The exact parent directory can vary, but the rule is stable: one report per directory.

## Compilation Workflow Examples

### Plain document

```sh
pdflatex main.tex
pdflatex main.tex
```

### Document with bibliography

```sh
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

If the document is configured for `biber` instead of `bibtex`, use `biber` in the bibliography step and then continue the `pdflatex` passes.

## Minimal Starting Points

### General report

```tex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{libertine}

\title{Report Title}
\author{Author Name}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
Write the report here.

\end{document}
```

### ACM-style conference draft

```tex
\documentclass[sigconf]{acmart}

\title{Paper Title}
\author{Author Name}

\begin{document}
\maketitle

\section{Introduction}
Write the paper here.

\end{document}
```

Use the ACM template only when it matches the requested venue or when ACM conference formatting is the intended default.

## Cross-References

- Follow the venue's official author kit, template, and formatting rules when the report targets a named conference or journal
- Use `git-checkpoint` when the report work should go through the repository's normal branch, commit, and PR workflow
- Use `writing-skills` if the task is to package report-generation guidance as another reusable skill rather than produce a report
- Use `writing-plugins` if the task is to distribute LaTeX/report workflows as an installable plugin instead of only authoring a report

## Done Criteria

- `pdflatex` availability confirmed before attempting PDF generation
- Report source placed in its own dedicated directory
- Document class and layout match the venue requirements or the default general-writeup rules
- Modern font choice used instead of built-in defaults unless the template requires otherwise
- LaTeX source compiles to a PDF without ignoring unresolved errors
- Compiled PDF updated and committed together with the source changes
- Directory contents are limited to that report's source, assets, and compiled artifacts

## Best Practices for LaTeX Reports

1. **Let the venue override the default** — conference and journal rules beat personal preferences.
2. **Keep each report isolated** — separate directories prevent asset collisions and confusing build artifacts.
3. **Treat the PDF as part of the deliverable** — if the source changed, rebuild and commit the PDF.
4. **Prefer simple, stable defaults** — `article` plus 1-inch margins is the fallback for ordinary writeups when no venue template is required.
5. **Fail clearly when LaTeX tooling is missing** — missing `pdflatex` is a blocker, not something to work around by claiming the report is done.
