## This document has Armenian text (XeLaTeX) and a glossary (makeglossaries).
## `latexmk -xelatex main.tex` then runs everything automatically.
$pdf_mode = 5;   # 5 = xelatex

# --- glossaries support ---
add_cus_dep('acn', 'acr', 0, 'makeglossaries');
add_cus_dep('glo', 'gls', 0, 'makeglossaries');
sub makeglossaries {
    my ($base_name, $path) = fileparse($_[0]);
    my @args = ("-d", $path, $base_name);
    if ($silent) { unshift @args, "-q"; }
    return system("makeglossaries", @args);
}
push @generated_exts, 'glo', 'gls', 'glg', 'acn', 'acr', 'alg', 'ist';
