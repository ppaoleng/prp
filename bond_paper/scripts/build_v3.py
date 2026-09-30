"""Build Bond_RB_GFRP_manuscript_v3.docx from the v2 file (v2 is never modified).
New/placeholder content is inserted in RED so that it can be found and removed."""
import copy, re, sys
import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from PIL import Image
import math

SRC = sys.argv[1]; OUT = sys.argv[2]; FIG = "/home/user/prp/bond_paper/figs/"
d = docx.Document(SRC)
W = nsdecls("w")
RED = "FF0000"
log = []          # (location, old, new) wording-change log

def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def find(prefix, nth=0):
    hits = [p for p in d.paragraphs if p.text.startswith(prefix)]
    assert hits, prefix
    return hits[nth]

def replace_text(p, old, new, where=""):
    runs = [r for r in p.runs if r._r.find(qn("w:t")) is not None]
    full = "".join(r.text for r in runs)
    i = full.find(old); assert i >= 0, (where, old[:60])
    j = i + len(old); pos = 0; first = True
    for r in runs:
        s, e = pos, pos + len(r.text); pos = e
        if e <= i or s >= j: continue
        a, b = max(i, s) - s, min(j, e) - s
        t = r.text
        r.text = t[:a] + (new if first else "") + t[b:]
        first = False
    log.append((where, old, new))

def red_run_xml(text, bold=False, size=None, italic=False):
    rpr = "<w:rPr>" + ("<w:b/>" if bold else "") + ("<w:i/>" if italic else "") + f'<w:color w:val="{RED}"/>' + (f'<w:sz w:val="{size}"/>' if size else "") + "</w:rPr>"
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def append_red(p, text):
    p._p.append(parse_xml(red_run_xml(" " + text, size=19 if p.text[:4] in ("Fig.", "Tabl") else None).replace("<w:r>", f"<w:r {W}>", 1)))

def red_par_after(ref, segs, ppr='<w:ind w:firstLine="425"/><w:jc w:val="both"/>', size=None):
    runs = "".join(red_run_xml(t, bold=b, size=size) for t, b in segs)
    el = parse_xml(f'<w:p {W}><w:pPr>{ppr}</w:pPr>{runs}</w:p>')
    (ref._p if hasattr(ref, "_p") else ref).addnext(el)
    return el

def caption_after(ref, label, text):
    ppr = '<w:keepNext/><w:spacing w:before="160" w:after="60" w:line="264" w:lineRule="auto"/>'
    return red_par_after(ref, [(label, True), (" " + text, False)], ppr=ppr, size=19)

def table_after(ref, header, rows, widths, note=None, bold_first_col=False):
    n = len(header)
    def cell(t, w, bold=False, top=None, bot=None, jc="left"):
        b = ""
        if top or bot:
            b = "<w:tcBorders>" + (f'<w:top w:val="single" w:sz="{top}" w:space="0" w:color="000000"/>' if top else "") + (f'<w:bottom w:val="single" w:sz="{bot}" w:space="0" w:color="000000"/>' if bot else "") + "</w:tcBorders>"
        return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{b}</w:tcPr><w:p><w:pPr><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/><w:jc w:val="{jc}"/></w:pPr>'
                + red_run_xml(t, bold=bold, size=17) + "</w:p></w:tc>")
    x = f'<w:tbl {W}><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/><w:tblLayout w:type="fixed"/></w:tblPr><w:tblGrid>' + "".join(f'<w:gridCol w:w="{w}"/>' for w in widths) + "</w:tblGrid>"
    x += '<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>' + "".join(cell(h, w, True, top=12, bot=6, jc=("left" if k == 0 else "center")) for k, (h, w) in enumerate(zip(header, widths))) + "</w:tr>"
    for ri, row in enumerate(rows):
        last = ri == len(rows) - 1
        x += '<w:tr><w:trPr><w:cantSplit/></w:trPr>' + "".join(cell(t, w, bold=(bold_first_col and k == 0), bot=(12 if last else None), jc=("left" if k == 0 else "center")) for k, (t, w) in enumerate(zip(row, widths))) + "</w:tr>"
    x += "</w:tbl>"
    tbl = parse_xml(x); (ref._p if hasattr(ref, "_p") else ref).addnext(tbl)
    last = tbl
    if note:
        last = red_par_after(tbl, [(note, False)], ppr='<w:spacing w:before="40" w:after="160" w:line="240" w:lineRule="auto"/><w:jc w:val="both"/>', size=17)
    return last

# ======================= 1. replace figures =======================
rid_fig = {f"rId{8 + k}": f"fig{k + 1}.png" for k in range(9)}
for rid, fn in rid_fig.items():
    part = d.part.related_parts[rid]; part._blob = open(FIG + fn, "rb").read()
    w, h = Image.open(FIG + fn).size
    for dr in d.element.body.iter(qn("w:drawing")):
        blip = [b for b in dr.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip") if b.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed") == rid]
        if not blip: continue
        cx = int(dr.find(".//" + qn("wp:extent")).get("cx")); cy = round(cx * h / w)
        dr.find(".//" + qn("wp:extent")).set("cy", str(cy))
        for e in dr.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}ext"): e.set("cy", str(cy)); e.set("cx", str(cx))

# ======================= 2. wording edits =======================
ab = find("Load passes between")
replace_text(ab, "Cement mortar was ineffective on plain bars, and grout differed from epoxy only at 14.7 MPa or above.", "Cement mortar was ineffective on plain bars.", "Abstract (duplicated sentence)")
replace_text(ab, "Strengths were nominal and groups small (n = 5), so the values are indicative; design use needs tests on the actual bar–agent–concrete combination.",
             "Concrete strengths were nominal grades (companion cubes were not crushed in the original tests) and each group had only five specimens, so the values are indicative only; design use requires tests on the actual bar–agent–concrete combination.", "Abstract (last sentence)")
p21 = find("Three features of this origin")
replace_text(p21, "the confirmatory analysis is confined", "the inferential analysis is confined", "Sec. 2.1 (confirmatory vs descriptive p values)")
pc = find("Concrete. All mixtures")
replace_text(pc, "the last two differ in the recorded curing period only (Table 2)", "the last two differ only in the recorded curing period, 7 d and 14 d (Table 2)", "Sec. 2.2 Concrete")
replace_text(pc, "so the strengths quoted in this paper are nominal grades, and the possible consequences are discussed in Section 4.2.", "so the strengths quoted in this paper are nominal grade labels and not measured values; the possible consequences are discussed in Section 4.2.", "Sec. 2.2 Concrete")
p23 = find("Cubes of 150 mm were cast")
replace_text(p23, "the bar was dipped in the freshly mixed agent and pushed into the hole", "the bar was coated by dipping it in the freshly mixed agent and was then pushed into the hole", "Sec. 2.3 installation")
p24 = find("Each cube was tested in direct pull-out")
replace_text(p24, "Peak load P was taken as the bond capacity.", "The peak load P was taken as the pull-out capacity of the specimen.", "Sec. 2.4")
replace_text(p24, "Slip records are not analysed here.", "Load–slip records are not analysed in this paper.", "Sec. 2.4")
p34 = find("Eight of 45") if False else find("For epoxy, the nominal bar stress at peak load")
replace_text(p34, "approached the catalogue yield level in part of the series", "reached or exceeded the catalogue yield level in part of the series", "Sec. 3.4 (8 of 45 specimens exceeded 235 MPa)")
p35 = find("One failure mode was recorded per plain-bar group")
replace_text(p35, "or by zero-bond slip-out (2)", "or by zero-bond slip-out, in which the bar was withdrawn without recorded resistance (2)", "Sec. 3.5 (term defined at first use)")
p36 = find("Table 7 lists the nine GFRP groups")
replace_text(p36, "though unevenly", "although not uniformly across diameters", "Sec. 3.6")
p36b = find("At the upper end of the range, strength stopped")
replace_text(p36b, "a net change that is not consistent in sign", "a change whose sign differs among the three diameters", "Sec. 3.6")

# captions
c1 = find("Fig. 1."); append_red(c1, "[REVISION – dashed boxes mark the verification steps requested in review (Appendix S). Keep only the steps actually completed; TO CONFIRM.]")
c2 = find("Fig. 2."); replace_text(c2, "and slip is read at the free end).", "and slip is read at the free end). Hatching: dots, concrete; diagonal lines, steel bar; cross-hatching, bonding agent. GFRP bars were cast in place, without a bonding-agent annulus.", "Fig. 2 caption")
c3 = find("Fig. 3."); replace_text(c3, "light points are individual specimens, and points at zero are specimens that recorded no load.", "error bars are omitted for cement mortar, whose SD is below 0.1 MPa and smaller than the symbol.", "Fig. 3 caption")
append_red(c3, "[AUTHORS: re-plot Figs 3–5 and 9 from the raw specimen file before submission; the group SDs in v3 were transcribed from the v2 figure and checked against Table 3.]")
c4 = find("Fig. 4."); replace_text(c4, "(b) Mean τ by agent and bar diameter (n = 15 per point).", "(b) Mean τ with 95% confidence intervals by agent and bar diameter (n = 15 per point).", "Fig. 4 caption"); replace_text(c4, "Light points in (a) and (b) are individual specimens.", "Bar colour and hatching in (c) follow the agent legend in (a): epoxy, oblique lines; grout, dots; mortar, cross-hatching.", "Fig. 4 caption")
c5 = find("Fig. 5."); replace_text(c5, "(mean ± 1 SD, n = 5; light points are individual specimens)", "(mean ± 1 SD, n = 5)", "Fig. 5 caption")
c7 = find("Fig. 7."); replace_text(c7, "symbols are group means ± 1 SD, and dashed lines are", "symbols are group means ± 1 SD, translucent vertical bars are the minimum–maximum range of the five specimens, and dashed lines are", "Fig. 7 caption")
c9 = find("Fig. 9."); replace_text(c9, "(mean ± 1 SD, n = 15 per point; light points are specimens)", "(mean ± 1 SD, n = 15 per point)", "Fig. 9 caption")

# ======================= 3. red placeholders in the body =======================
POINT = '<w:ind w:firstLine="425"/><w:jc w:val="both"/>'
red_par_after(p21, [("[REVISION – reviewer comment 2] The origin of every specimen is to be documented in a traceability log (Table S5); groups without supporting records are to be removed from the analysis.", False)])
red_par_after(pc, [("[REVISION – reviewer comment 1] Companion 150 mm cubes from each mixture are to be crushed at the age of the pull-out test. Table S1 shows the layout with PLACEHOLDER values only. Nominal grades are retained throughout the paper until measured values exist.", False)])
ps = find("Steel bars. Plain round bars")
red_par_after(ps, [("[REVISION – reviewer comment 7] Tensile coupons of each bar size are to be tested; Table S2 shows the layout with PLACEHOLDER values. Sections 3.4 and 4.3 must be rewritten once measured yield strengths replace the catalogue value.", False)])
pg = find("GFRP bars. Bars of 6, 9, and 12 mm")
red_par_after(pg, [("[REVISION – reviewer comment 7] Manufacturer data and tensile properties of the GFRP bars are to be reported (Table S3, PLACEHOLDER values).", False)])
red_par_after(p24, [("[REVISION – reviewer comment 4] A supplementary series with le = 5 db (geometry of ACI 440.3R, Annex B.3) is laid out in Table S4 with PLACEHOLDER values, and load–slip curves from the LVDT records are to be added [TO CONFIRM that the records exist].", False)])
p46 = find("The specimen follows a withdrawn standard")
red_par_after(p46, [("[REVISION – reviewer comment 4] After the short-embedment series (Table S4) is tested, add here a comparison of the long-length average τ with the 5 db values, and reword the last sentence of this paragraph accordingly.", False)])
p48 = find("Concrete strength. Strengths are nominal grades")
append_red(p48, "[REVISE this limitation if the companion-cube results (Table S1) are adopted.]")
da = find("Data availability.")
append_red(da, "[ACTION – reviewer comment 2: obtain the raw UTM/LVDT files before submission. If raw records cannot be produced, remove the affected groups; do not state that the records are available.]")

# ======================= 4. Appendix S (all red) =======================
ack = find("Acknowledgements.")
h = parse_xml(f'<w:p {W}><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>{red_run_xml("Appendix S. Revision placeholders (replace or delete before submission)")}</w:p>')
ack._p.addnext(h)
w1 = red_par_after(h, [("WARNING. ", True), ("Every number in Tables S1–S4 is an ILLUSTRATIVE PLACEHOLDER written to show the expected layout and a plausible order of magnitude for this type of test. The values were not measured, are not in the v2 manuscript or its source projects, and must not be cited, used in any calculation, or submitted. Replace them with laboratory results or delete the tables. Table S5 is a blank checklist and contains no data.", False)])
cur = w1
cur = caption_after(cur, "Table S1.", "[PLACEHOLDER VALUES] Compressive strength of companion 150 mm cubes at the age of the pull-out test (reviewer comment 1).")
cur = table_after(cur, ["Nominal grade (MPa)", "Mixture", "Curing (d)", "Age at test (d)", "n", "Measured f′c, mean (SD) (MPa)", "CV (%)", "Measured / nominal"],
    [["4.9 (50 ksc)", "Dry mix + equal mass of sand", "5", "8", "3", "5.8 (0.6)", "10.3", "1.18"],
     ["14.7 (150 ksc)", "Dry mix", "7", "10", "3", "13.4 (1.0)", "7.5", "0.91"],
     ["23.5 (240 ksc)", "Dry mix", "14", "17", "3", "17.9 (1.3)", "7.3", "0.76"]],
    [1100, 1700, 850, 900, 420, 1500, 680, 1000], note="Age at test is curing period plus the 2–3 d between installation and testing recorded in Section 2.3 [TO CONFIRM]. Cube standard and loading rate: [TO CONFIRM].")
cur = caption_after(cur, "Table S2.", "[PLACEHOLDER VALUES] Tensile properties of the SR24 plain round bars from coupon tests (reviewer comment 7).")
cur = table_after(cur, ["Bar", "db (mm)", "Nominal area (mm²)", "n", "Yield strength fy, mean (SD) (MPa)", "Tensile strength fu, mean (SD) (MPa)", "fu / fy", "Elongation (%)"],
    [["RB6", "6", "28.3", "3", "352 (8)", "448 (6)", "1.27", "26"],
     ["RB9", "9", "63.6", "3", "326 (6)", "441 (5)", "1.35", "28"],
     ["RB12", "12", "113.1", "3", "305 (7)", "436 (6)", "1.43", "30"]],
    [700, 760, 1100, 420, 1600, 1600, 700, 1150], note="Catalogue minimum values used in v2: fy = 235 MPa, fu = 385 MPa. Yield point method and gauge length: [TO CONFIRM].")
cur = caption_after(cur, "Table S3.", "[PLACEHOLDER VALUES] Tensile properties of the GFRP bars (reviewer comment 7). Maximum observed loads are taken from Section 3.6 of the manuscript.")
cur = table_after(cur, ["Bar", "db (mm)", "Area (mm²)", "ffu, mean (SD) (MPa)", "Ef (GPa)", "εfu (%)", "Ffu (kN)", "Max observed P (kN)", "Max P / Ffu"],
    [["GF6", "6", "28.3", "1040 (36)", "46.5", "2.24", "29.4", "22.23", "0.76"],
     ["GF9", "9", "63.6", "905 (31)", "45.8", "1.98", "57.6", "24.18", "0.42"],
     ["GF12", "12", "113.1", "812 (28)", "45.1", "1.80", "91.8", "25.76", "0.28"]],
    [650, 700, 800, 1400, 750, 750, 800, 1200, 900], note="Manufacturer, surface treatment, fibre content and resin: [TO CONFIRM]. Ffu = ffu × area. Test method for ffu and Ef: [TO CONFIRM].")
# Table S4: compute P from tau so the rows are internally consistent
def row(bar, db, fc, n, tau, slip, mode):
    le = 5 * db; P = tau * math.pi * db * le / 1000.0
    return [bar, str(db), str(le), fc, str(n), f"{P:.1f}", f"{tau:.1f}", f"{slip:.2f}", mode]
rowsS4 = [row("GF6", 6, "14.7", 3, 10.9, .85, "Pull-out"), row("GF9", 9, "14.7", 3, 9.8, 1.10, "Pull-out"), row("GF12", 12, "14.7", 3, 9.1, 1.32, "Pull-out (2), splitting (1)"),
          row("GF6", 6, "23.5", 3, 12.6, .92, "Pull-out"), row("GF9", 9, "23.5", 3, 11.4, 1.21, "Pull-out"), row("GF12", 12, "23.5", 3, 10.6, 1.48, "Splitting (2), pull-out (1)"),
          row("RB6 epoxy", 6, "23.5", 3, 5.9, .64, "Pull-out"), row("RB9 epoxy", 9, "23.5", 3, 6.4, .77, "Pull-out"), row("RB12 epoxy", 12, "23.5", 3, 6.8, .86, "Pull-out")]
cur = caption_after(cur, "Table S4.", "[PLACEHOLDER VALUES] Supplementary pull-out series with bonded length le = 5 db (reviewer comment 4). Plain bars are epoxy-anchored; nominal strength is used until Table S1 is replaced by measured values.")
cur = table_after(cur, ["Specimen", "db (mm)", "le (mm)", "Nominal f′c (MPa)", "n", "Peak load P (kN)", "τ = P/(π db le) (MPa)", "Slip at peak (mm)", "Failure mode"],
    rowsS4, [1000, 620, 620, 900, 380, 900, 1250, 900, 1700],
    note="Peak load and τ are group means; P was computed from the listed τ so that the columns are mutually consistent. Specimen geometry, block size and loading rate: [TO CONFIRM against ACI 440.3R Annex B.3].")
cur = caption_after(cur, "Table S5.", "Data-provenance checklist (reviewer comment 2). Blank template – no data have been entered.")
cur = table_after(cur, ["Item", "Evidence needed", "Status"],
    [["Fifth specimen of every plain-bar group", "Specimen ID, casting date, test date, record of who tested it", "To be completed"],
     ["Repeated GFRP tests (25 of 45 values differ from the project report)", "Both sets of values, reason for repetition, raw load files of both", "To be completed"],
     ["Raw load–slip files (UTM and LVDT export)", "One file per specimen, with machine, rate and date", "To be completed"],
     ["Photographs and notebook pages", "Time-stamped images of each batch and test", "To be completed"],
     ["GFRP coefficients of variation of 2–7% (Section 3.6)", "Comparison against raw peak loads; explanation of low scatter", "To be completed"],
     ["Consent and data-sharing permission", "Written permission from the students for data and photographs", "To be completed"]],
    [3000, 4500, 1400])

d.save(OUT)
import json; json.dump(log, open("/home/user/prp/bond_paper/manuscript/wording_log.json", "w"), ensure_ascii=False, indent=1)
print("saved", OUT, len(log), "wording edits")
