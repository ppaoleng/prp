# Bond_RB_GFRP manuscript revision (v2 -> v3)

- `manuscript/Bond_RB_GFRP_manuscript_v3.docx` – revised manuscript (new/placeholder content in red).
- `manuscript/Bond_RB_GFRP_manuscript_v2_original.docx` – untouched copy of the submitted v2.
- `manuscript/Bond_RB_GFRP_revision_log_TH.docx` – Thai change log (reviewer comments, figures, wording old -> new).
- `figs/fig1.png … fig9.png` – redrawn figures (420 dpi, no text baked in).
- `scripts/` – one script per figure (`fig1_workflow.py` …), `fig_style.py`, `bond_data.py`, `build_v3.py`.
- `source/` – inputs copied from the upload (photo composite of v2 Fig. 2, reviewer comment file).

Rebuild: `cd scripts && for f in fig?_*.py; do python3 $f; done && cd .. && python3 scripts/build_v3.py manuscript/Bond_RB_GFRP_manuscript_v2_original.docx manuscript/Bond_RB_GFRP_manuscript_v3.docx`

**Data caveat.** Specimen-level data were not available. `scripts/bond_data.py` holds group means/SDs taken from the manuscript text and
tables and, for the plain-bar groups of Fig. 3, read from the v2 bitmap and cross-checked against Table 3 (see the docstring).
Replace that block with the raw specimen file and re-run the figure scripts. Tables S1–S4 in the .docx are illustrative placeholders, not measurements.
