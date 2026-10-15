# diagrams/
One TikZ picture per file (only the `tikzpicture` environment). Insert with
`\adddiagram[label]{file-name-without-.tex}{width-fraction}{Caption.}`.
Colors `briefaccent` and `brieflight` match the document. For complex drawings,
export a vector PDF from draw.io / Inkscape into `images/` and use `\addimage`.
