# Markdown readings and materials

A `.md` file in `readings` (or `materials`) is shown in SemiTec Academy's document reader (app ≥ 1.3.0).

**Supported** — GitHub-flavoured Markdown:
headings (`#`–`######`; `#`–`###` form the outline), paragraphs, **bold**, *italic*, `code`, links,
bulleted / numbered / task lists, block quotes, tables, fenced code blocks with a language
(```` ```systemverilog ````) and a *Copy* button, horizontal rules, images.

**Images and linked files** must be next to the `.md` file or in a subfolder (`images/x.png`,
`img/diagram.svg`). The checker finds every local image and link, reports missing files and files
outside the document's folder, and packs them together with the document. Links to other `.md` files
of the same reading open in the reader (with a *Back* link); web links open in the browser.

**Not supported / removed for safety:** scripts, iframes, forms and inline event handlers (the HTML is
sanitised), LaTeX math, Mermaid diagrams (use an SVG image instead).

**Reading progress:** the part of the document scrolled through; completed at 90 % or with
*Mark as finished*. The reader remembers the position. Students can change the text size.

Tips: start with one `# Title`, use `##` for sections (they become the outline), keep images SVG or PNG
under ~1 MB, write code blocks with a language name.
