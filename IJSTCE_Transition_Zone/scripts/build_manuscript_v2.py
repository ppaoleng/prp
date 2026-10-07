"""Build manuscript v2: (1) replace Figs. 1-6 with the redrawn PNGs, (2) minimal caption edits for Figs. 4-6,
(3) insert Thai review comments as yellow-highlighted [AI-nn ...] runs.

The original .docx is never modified: a new file is written to --out.
Usage: python3 build_manuscript_v2.py --src ORIGINAL.docx --figs ../figures --out OUT.docx
"""
import argparse, copy, re, sys, zipfile
from pathlib import Path
from lxml import etree
from PIL import Image

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
XML_NS = "http://www.w3.org/XML/1998/namespace"
q = lambda t: "{%s}%s" % (W, t)

# figure -> (media file, placed width in inches)
FIGS = [("Fig1_workflow.png", "image1.png", 6.5), ("Fig2_schematic.png", "image2.png", 6.5),
        ("Fig3_stiffness.png", "image3.png", 5.0), ("Fig4_force_speed.png", "image4.png", 5.0),
        ("Fig5_reduction.png", "image5.png", 5.4), ("Fig6_force_vs_stiffness.png", "image6.png", 5.0)]

# caption edits: (paragraph starts with, old text, new text)
CAPTION_EDITS = [
    ("Fig. 4", "(AR, auxiliary rail; ES, enlarged sleepers).",
     "(AR, auxiliary rail; ES, enlarged sleepers). The inset shows an enlarged view of M3–M5."),
    ("Fig. 5", "at four train speeds. The values above the bars are those at 120 km/h.",
     "at four train speeds (AR, auxiliary rail; ES, enlarged sleepers). The values above the bars are the reductions in percent."),
    ("Fig. 6", "approach-side stiffness of M1 to M5.",
     "approach-side stiffness of M1 to M5. Dotted lines join M1, M2, M3 and M5, and the labels give the change in force per unit of added stiffness (kN per kN/mm) quoted in Sect. 3.4."),
]


def ptext(p, skip_comments=True):
    return "".join(run_text(r) for r in p if r.tag == q("r") and not (skip_comments and is_comment(r)))


def run_text(r):
    return "".join(t.text or "" for t in r.findall(q("t")))


def is_comment(r):
    rpr = r.find(q("rPr"))
    return rpr is not None and rpr.find(q("highlight")) is not None


def mk_t(text):
    t = etree.Element(q("t")); t.text = text; t.set("{%s}space" % XML_NS, "preserve"); return t


def comment_run(text):
    r = etree.Element(q("r")); rpr = etree.SubElement(r, q("rPr"))
    f = etree.SubElement(rpr, q("rFonts"))
    for k in ("ascii", "hAnsi", "cs", "eastAsia"):
        f.set(q(k), "Tahoma")
    etree.SubElement(rpr, q("sz")).set(q("val"), "19")
    etree.SubElement(rpr, q("szCs")).set(q("val"), "19")
    etree.SubElement(rpr, q("highlight")).set(q("val"), "yellow")
    etree.SubElement(rpr, q("lang")).set(q("bidi"), "th-TH")
    r.append(mk_t(text)); return r


def plain_space_like(run):
    r = etree.Element(q("r"))
    rpr = run.find(q("rPr"))
    if rpr is not None and rpr.find(q("highlight")) is None:
        r.append(copy.deepcopy(rpr))
    r.append(mk_t(" ")); return r


def split_run(run, offset):
    """Split run at text offset; returns the run holding the first part (second part inserted after it)."""
    txt = run_text(run)
    second = copy.deepcopy(run)
    for t in run.findall(q("t")): run.remove(t)
    for t in second.findall(q("t")): second.remove(t)
    run.append(mk_t(txt[:offset])); second.append(mk_t(txt[offset:]))
    run.addnext(second); return run


def insert_after_text(p, anchor_end, text):
    """Insert a comment run right after `anchor_end` (or at paragraph end when None)."""
    runs = [r for r in p if r.tag == q("r") and not is_comment(r)]
    if anchor_end is None:
        target = runs[-1] if runs else None
    else:
        full = "".join(run_text(r) for r in runs)
        pos = full.find(anchor_end)
        assert pos >= 0 and full.count(anchor_end) >= 1, f"anchor not found: {anchor_end!r}"
        end = pos + len(anchor_end); cum = 0; target = None
        for r in runs:
            n = len(run_text(r))
            if cum < end <= cum + n:
                target = r if end == cum + n else split_run(r, end - cum)
                break
            cum += n
        assert target is not None
    sp = plain_space_like(target); cr = comment_run(text)
    # keep comments in order when several are appended after the same run
    nxt = target.getnext()
    while nxt is not None and nxt.tag == q("r") and is_comment(nxt):
        target = nxt; nxt = target.getnext()
    target.addnext(sp); sp.addnext(cr)


def find_para(body, contains, nth=0):
    hits = [p for p in body.iter(q("p")) if contains in ptext(p)]
    assert len(hits) > nth, f"paragraph not found: {contains!r} ({len(hits)} hits)"
    if nth == 0 and len(hits) > 1:
        print(f"  note: {len(hits)} paragraphs match {contains!r}; using the first", file=sys.stderr)
    return hits[nth]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True); ap.add_argument("--figs", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--comments", default=str(Path(__file__).with_name("comments_th.py")))
    a = ap.parse_args()
    ns = {}; exec(Path(a.comments).read_text(encoding="utf8"), ns)
    COMMENTS = ns["COMMENTS"]

    zin = zipfile.ZipFile(a.src)
    root = etree.fromstring(zin.read("word/document.xml"))
    body = root.find(q("body"))

    # abstract word count (for the comment text)
    abs_p = find_para(body, "Stiffness discontinuity between ballasted track and a bridge")
    n_words = len(ptext(abs_p).split())
    print("abstract words:", n_words)

    # 1) figures: resize drawing extents
    media = {}
    drawings = list(root.iter("{%s}inline" % WP))
    assert len(drawings) == 6, len(drawings)
    for d, (png, mname, width_in) in zip(drawings, FIGS):
        with Image.open(Path(a.figs) / png) as im:
            wpx, hpx = im.size
        cx = int(width_in * 914400); cy = int(cx * hpx / wpx)
        d.find("{%s}extent" % WP).attrib.update({"cx": str(cx), "cy": str(cy)})
        ext = d.find(".//{%s}ext" % A); ext.set("cx", str(cx)); ext.set("cy", str(cy))
        media["word/media/" + mname] = (Path(a.figs) / png).read_bytes()
        print(f"  {png}: {wpx}x{hpx}px -> {width_in:.2f} x {width_in*hpx/wpx:.2f} in ({wpx/width_in:.0f} ppi at placed size)")

    # 2) caption edits
    for start, old, new in CAPTION_EDITS:
        done = False
        for p in body.iter(q("p")):
            if ptext(p).startswith(start + " ") or ptext(p).startswith(start):
                for r in p:
                    if r.tag == q("r") and old in run_text(r):
                        t = r.find(q("t")); t.text = run_text(r).replace(old, new); done = True; break
            if done: break
        assert done, f"caption edit failed: {start}"

    # 3) comments
    for i, (pc, anchor, text) in enumerate(COMMENTS, 1):
        p = find_para(body, pc)
        insert_after_text(p, anchor, "[AI-%02d %s]" % (i, text.replace("{n_words}", str(n_words))))
    print("comments inserted:", len(COMMENTS))

    xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    with zipfile.ZipFile(a.out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml": data = xml
            elif item.filename in media: data = media[item.filename]
            zout.writestr(item, data)
    print("written:", a.out)


if __name__ == "__main__":
    main()
