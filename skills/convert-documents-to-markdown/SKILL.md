---
name: convert-documents-to-markdown
description: >-
  Extract Markdown from PDFs and other document formats by installing and
  invoking Microsoft MarkItDown from the command line. Use when an agent needs
  to read a PDF, Word document, PowerPoint, spreadsheet, HTML file, EPUB, or
  similar source by converting it into Markdown first.
license: MIT
---

# Converting Documents to Markdown with MarkItDown

This skill explains how to read non-Markdown documents by converting them into Markdown first with [Microsoft MarkItDown](https://github.com/microsoft/markitdown). MarkItDown is a Python utility that converts formats such as PDF, Word, PowerPoint, Excel, HTML, EPUB, CSV, JSON, XML, ZIP archives, and more into Markdown that agents can inspect and reason about more effectively.

For final critique of the extracted or rewritten Markdown, see `review-document`. For authoring reusable skills like this one, see `writing-skills`.

## Procedure

1. **Inspect First** — identify the input file type, whether you only need PDF support or broader document coverage, and whether the environment already has MarkItDown installed.
2. **Check whether MarkItDown is available** — run:

   ```powershell
   python -m pip show markitdown
   ```

   If it is already installed, continue. If not, install it in the current environment.
3. **Install the right dependency set** — prefer the smallest extra set that covers the needed formats:

   ```powershell
   # PDF only
   python -m pip install "markitdown[pdf]"

   # Broad document support
   python -m pip install "markitdown[all]"
   ```

   `markitdown[all]` is the safest default when the agent may need to handle multiple document types in one workflow.
4. **Prefer `python -m markitdown` on Windows** — the `markitdown` console script may not be on `PATH` even when the package is installed. `python -m markitdown` avoids that issue and was verified in this environment.
5. **Convert the file to Markdown** — the two primary invocation patterns are:

   ```powershell
   # Write Markdown to stdout
   python -m markitdown C:\path\to\document.pdf > C:\path\to\document.md

   # Or write directly to a file
   python -m markitdown C:\path\to\document.pdf -o C:\path\to\document.md
   ```

   The same pattern works for other supported files such as `.docx`, `.pptx`, `.xlsx`, `.html`, `.epub`, `.csv`, `.json`, and `.xml`.
6. **Read the extracted Markdown rather than the binary source** — once conversion succeeds, inspect the generated `.md` file with the normal file-reading tools. This is the point where the agent effectively "reads the PDF" or other document.
7. **Spot-check extraction quality** — verify that the Markdown contains the expected headings, paragraphs, lists, and tables. If the output is truncated, malformed, or unexpectedly sparse, keep the original file around and note the extraction limitation explicitly.
8. **Use format hints only when needed** — if the filename or extension is ambiguous, consult the tested CLI help:

   ```powershell
   python -m markitdown --help
   ```

   The CLI supports hints such as `-x` (extension), `-m` (MIME type), and `-c` (charset) for edge cases where the file type is not obvious.
9. **Escalate to broader dependencies only when necessary** — if PDF conversion works but another format fails, install the needed extra (or `markitdown[all]`) rather than assuming the base install supports every format.

## Tested Commands

These command patterns were verified in this environment:

```powershell
python -m pip install "markitdown[pdf]"
python -m markitdown C:\path\to\sample.pdf > C:\path\to\sample.md
python -m markitdown C:\path\to\sample.pdf -o C:\path\to\sample.md
```

In this Windows environment, `python -m markitdown` worked, while the bare `markitdown` executable was not available on `PATH`.

## Common Use Cases

| Input | Example command |
|-------|-----------------|
| **PDF** | `python -m markitdown paper.pdf -o paper.md` |
| **Word** | `python -m markitdown report.docx -o report.md` |
| **PowerPoint** | `python -m markitdown slides.pptx -o slides.md` |
| **Spreadsheet** | `python -m markitdown data.xlsx -o data.md` |
| **HTML** | `python -m markitdown page.html -o page.md` |

## Notes and Caveats

- MarkItDown focuses on useful Markdown extraction for LLMs and analysis pipelines, not pixel-perfect document reproduction.
- Optional dependencies are organized by feature group. A successful base install does **not** guarantee that every format is enabled.
- Some PDFs may emit warnings about metadata or extraction permissions while still converting successfully.
- If you see unrelated warnings about tools such as `ffmpeg`, do not assume PDF conversion failed; inspect the Markdown output itself.

## Rules and Constraints

- Do **not** try to parse PDF bytes manually when MarkItDown is available.
- Do **not** assume the `markitdown` executable is callable directly on Windows.
- Do **not** cite a document as "read" until the Markdown extraction has succeeded and the output has been inspected.
- Do **not** silently ignore poor extraction quality; record limitations when conversion is lossy or incomplete.
- Do **not** install `markitdown[all]` by reflex if only a narrow format set is needed, unless the workflow clearly benefits from broad support.

## Done Criteria

- The file type and required coverage were identified up front
- MarkItDown availability was checked
- Missing dependencies were installed with the appropriate extras
- The document was converted to Markdown with a tested CLI command
- The generated Markdown was inspected instead of the raw binary file
- Extraction quality or limitations were noted when relevant
