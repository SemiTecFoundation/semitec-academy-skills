## latexmk configuration: makes `latexmk -pdf main.tex` run bibtex AND the
## glossary step automatically, so one command builds the whole PDF.
$pdf_mode = 1;
$bibtex_use = 2;

# --- glossaries support (official snippet) ---
add_cus_dep('acn', 'acr', 0, 'makeglossaries');
add_cus_dep('glo', 'gls', 0, 'makeglossaries');
sub makeglossaries {
    my ($base_name, $path) = fileparse($_[0]);
    my @args = ("-d", $path, $base_name);
    if ($silent) { unshift @args, "-q"; }
    return system("makeglossaries", @args);
}
push @generated_exts, 'glo', 'gls', 'glg', 'acn', 'acr', 'alg', 'ist';
