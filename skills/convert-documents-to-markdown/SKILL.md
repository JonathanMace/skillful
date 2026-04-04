---
name: convert-documents-to-markdown
description: >-
  Extract Markdown from PDFs and other document formats by installing and
  invoking Microsoft MarkItDown from the command line.  Use when an agent needs
  to read a PDF, Word document, PowerPoint, spreadsheet, HTML file, EPUB, or
  similar source by converting it into Markdown first.
license: MIT
---

# Converting Documents to Markdown with MarkItDown

Read non-Markdown documents by converting them to Markdown with [Microsoft MarkItDown](https://github.com/microsoft/markitdown). MarkItDown is a Python CLI that converts PDF, Word, PowerPoint, Excel, HTML, EPUB, CSV, JSON, XML, ZIP archives, and more into Markdown that agents can inspect and reason about directly.

## Procedure

1. **Inspect First** — identify the input file type, whether you need only PDF support or broader document coverage, and whether the environment already has MarkItDown installed:

   ```powershell
   python -m pip show markitdown
   ```

2. **Install the right dependency set** — if MarkItDown is missing or the installed extras do not cover the needed format, install the smallest extra set that does. Text-based formats (HTML, CSV, JSON, XML) work with a base `pip install markitdown`; binary formats need extras:

   | Format | Install command |
   |--------|----------------|
   | HTML, CSV, JSON, XML | `pip install markitdown` (base) |
   | PDF | `pip install "markitdown[pdf]"` |
   | Word (.docx) | `pip install "markitdown[docx]"` |
   | PowerPoint (.pptx) | `pip install "markitdown[pptx]"` |
   | Excel (.xlsx) | `pip install "markitdown[xlsx]"` |
   | Multiple formats | `pip install "markitdown[pdf,docx,pptx]"` |
   | Everything | `pip install "markitdown[all]"` |

   Prefer the narrow install. Use `markitdown[all]` only when the workflow clearly needs multiple format families.

3. **Convert the file to Markdown** — always invoke via `python -m markitdown` (the bare `markitdown` console script may not be on `PATH`, especially on Windows):

   ```powershell
   # Write to stdout
   python -m markitdown document.pdf > document.md

   # Write directly to a file
   python -m markitdown document.pdf -o document.md
   ```

   The same pattern works for `.docx`, `.pptx`, `.xlsx`, `.html`, `.epub`, `.csv`, `.json`, `.xml`, and other supported types.

4. **Read the extracted Markdown, not the binary source** — once conversion succeeds, inspect the generated `.md` file with normal file-reading tools. This is the point where the agent effectively "reads" the document.

5. **Spot-check extraction quality** — verify that the Markdown contains the expected headings, paragraphs, lists, and tables. If the output is truncated or unexpectedly sparse, keep the original file and note the limitation explicitly.

6. **Use format hints for ambiguous files** — if the filename or extension is unclear, pass hints to the CLI:

   ```powershell
   python -m markitdown --help   # shows -x (extension), -m (MIME type), -c (charset)
   ```

## Common Use Cases

| Input | Example command |
|-------|-----------------|
| **PDF** | `python -m markitdown paper.pdf -o paper.md` |
| **Word** | `python -m markitdown report.docx -o report.md` |
| **PowerPoint** | `python -m markitdown slides.pptx -o slides.md` |
| **Spreadsheet** | `python -m markitdown data.xlsx -o data.md` |
| **HTML** | `python -m markitdown page.html -o page.md` |

## Rules and Constraints

- Do **not** parse binary document bytes manually when MarkItDown is available.
- Do **not** assume the bare `markitdown` executable is on `PATH`; use `python -m markitdown`.
- Do **not** cite a document as "read" until the Markdown extraction has succeeded and the output has been inspected.
- Do **not** silently ignore poor extraction quality; record limitations when conversion is lossy or incomplete.
- Do **not** install `markitdown[all]` by reflex if only a narrow format set is needed.
- MarkItDown focuses on useful extraction for LLMs, not pixel-perfect reproduction. Expect best-effort fidelity.
- Optional dependencies are organized by feature group — a base install does **not** guarantee every format.
- Warnings about unrelated tools (e.g., `ffmpeg`) do not mean conversion failed; always inspect the output.

## Cross-References

- Use `review-document` for critical review of extracted or rewritten Markdown after conversion
- Use `writing-skills` if the task is to package document-conversion guidance as a reusable skill rather than convert a document

## Done Criteria

- Input file type and required format coverage identified up front
- MarkItDown availability checked; missing extras installed
- Document converted to Markdown via `python -m markitdown`
- Generated Markdown inspected instead of the raw binary file
- Extraction quality or limitations noted when relevant
