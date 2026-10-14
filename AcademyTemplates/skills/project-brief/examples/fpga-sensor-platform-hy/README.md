# Example — FPGA sensor platform (cross-department, Armenian, reformed spelling)

A complete brief built with the `project-brief` template: two students
(Microelectronics + Software/CE), AMD AUP ZU3 (Zynq UltraScale+), Armenian with
reformed spelling. Compiled result: `brief.pdf`.

It reuses the content of the earlier task definition
(`diploma-project/examples/fpga-sensor-platform-hy`). The new parts were added
as an illustration and should be reviewed by the supervisors before use:
learning outcomes, out-of-scope items, interfaces, learning path, warm-up
exercises, work plan, deliverables, rubric and risks.

Shows: cross-department mode, the technical description split into three chapters
(`05a`–`05c`), per-student task lists and learning-path tables, an interfaces
table, TikZ diagrams, a register map, a reading list (BibLaTeX), and one
remaining `\missing{}` marker (a source still to verify).

Build: `latexmk -xelatex main.tex`
