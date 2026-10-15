# diagrams/

One **TikZ** diagram per file. Each file contains *only* the picture — no document
wrapper:

```latex
\begin{tikzpicture}[...]
  ...
\end{tikzpicture}
```

Insert it in a section with:

```latex
\adddiagram[fig:label]{filename}{0.8}{Your caption.}
```

`filename` is the name **without** the `.tex` extension; `0.8` is the width as a
fraction of the text width; the diagram is centered and captioned automatically.

See `example-architecture.tex` for a working example. TikZ libraries already
loaded: `positioning`, `arrows.meta`, `shapes.geometric`, `calc` (add more in
`diplomastyle.sty` if needed).

For complex diagrams, draw them in a tool that exports **vector PDF** (draw.io,
Inkscape, tikzit) and include the PDF via `\addimage` from `images/` instead.
