# labstyle.sty — commands

| Command | Use |
|---|---|
| `\usepackage[english]{labstyle}` | language: `english`, `armenian`, `armenian-classical`; add `draft` for a DRAFT mark |
| `\setlabtitle{…}` `\setlabnumber{1}` `\setlabid{lab-01-x}` `\setcourse{…}` | title block (see `metadata.tex` for all fields) |
| `\setduration{…}` `\setdifficulty{beginner\|intermediate\|advanced}` `\setgroupsize{…}` `\setversion{…}` | "Lab at a glance" tiles |
| `\setequipment{…}` `\setsoftware{…}` `\setprerequisites{…}` `\setauthor{…}` `\setdepartment{…}` | "Lab at a glance" rows |
| `\makelabtitle` | title band + lab-at-a-glance card |
| `\begin{objectives} \item … \end{objectives}` | objectives list |
| `\labstep[file1,file2]{id}{Title}` | numbered procedure step; `id` = step id in `lab.json`; files shown as chips |
| `\stepref{id}` | "Step 3" reference |
| `\expected{…}` | green "Expected result:" line |
| `\checkpoint{…}` `\notebox{…}` `\tipbox{…}` `\safetybox{…}` | callout boxes |
| `\srcfile[Language]{src/path}{caption}` | include a file from `lab/` (default language SystemVerilog; also Verilog, VHDL, C, Python, tcl …) |
| `\begin{lstlisting}[language=SystemVerilog] … \end{lstlisting}` | short code |
| `\adddiagram[label]{file}{width}{caption}` | TikZ picture from `diagrams/file.tex` |
| `\addimage[label]{images/x.png}{width}{caption}` | image |
| `\begin{measurements}[caption] \measure{quantity}{expected}{unit} \end{measurements}` | table with an empty "Measured" column |
| `\begin{questions} \question … \end{questions}` | numbered questions Q1, Q2 … |
| `\begin{assessment} \criterion{what}{weight} \end{assessment}` | grading table |
| `\missing{…}` / `\setnomissingcheck` | red placeholder / hide all placeholders |
| `\printreferences` | references from `references.bib` |

Colours: `labaccent`, `labgray`, `lablight`, `labgood`, `labwarn`, `labdanger` (usable in TikZ).
