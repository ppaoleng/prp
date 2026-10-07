"""Round 2: take the authors' V2 .docx, (1) swap selected figure images, (2) insert Thai review comments
as yellow-highlighted [AI2-nn ...] runs. The body text of V2 is not changed; the input file is never modified.

Usage: python3 build_manuscript_v3.py --src V2.docx --figs ../figures --out V3.docx \
         --replace Fig1_workflow.png=image1.png --replace Fig2_schematic.png=image2.png
"""
import argparse, copy, re, sys, zipfile
from pathlib import Path
from lxml import etree
from PIL import Image

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
      "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "rel": "http://schemas.openxmlformats.org/package/2006/relationships"}
W = NS["w"]; XML_NS = "http://www.w3.org/XML/1998/namespace"
q = lambda t: "{%s}%s" % (W, t)


def run_text(r):
    return "".join(t.text or "" for t in r.findall(q("t")))


def is_comment(r):
    rpr = r.find(q("rPr"))
    return rpr is not None and rpr.find(q("highlight")) is not None


def ptext(p):
    return "".join(run_text(r) for r in p if r.tag == q("r") and not is_comment(r))


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


def plain_space():
    r = etree.Element(q("r")); r.append(mk_t(" ")); return r


def split_run(run, offset):
    txt = run_text(run)
    second = copy.deepcopy(run)
    for t in run.findall(q("t")): run.remove(t)
    for t in second.findall(q("t")): second.remove(t)
    run.append(mk_t(txt[:offset])); second.append(mk_t(txt[offset:]))
    run.addnext(second); return run


def insert_after_text(p, anchor_end, text):
    runs = [r for r in p if r.tag == q("r") and not is_comment(r) and r.find(q("t")) is not None]
    full = "".join(run_text(r) for r in runs)
    if anchor_end is None:
        target = runs[-1]
    else:
        pos = full.find(anchor_end)
        assert pos >= 0, f"anchor not found: {anchor_end!r}"
        end = pos + len(anchor_end); cum = 0; target = None
        for r in runs:
            n = len(run_text(r))
            if cum < end <= cum + n:
                target = r if end == cum + n else split_run(r, end - cum)
                break
            cum += n
        assert target is not None
    nxt = target.getnext()
    while nxt is not None and nxt.tag == q("r") and is_comment(nxt):
        target = nxt; nxt = target.getnext()
    sp = plain_space(); cr = comment_run(text)
    target.addnext(sp); sp.addnext(cr)


def find_para(body, contains):
    hits = [p for p in body.iter(q("p")) if contains in ptext(p)]
    assert hits, f"paragraph not found: {contains!r}"
    if len(hits) > 1:
        print(f"  note: {len(hits)} paragraphs match {contains!r}; using the first", file=sys.stderr)
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True); ap.add_argument("--figs", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--replace", action="append", default=[], help="PNG=imageN.png (file in --figs replaces word/media/imageN.png)")
    ap.add_argument("--comments", default=str(Path(__file__).with_name("comments_th_r2.py")))
    ap.add_argument("--prefix", default="AI2")
    a = ap.parse_args()
    ns = {}; exec(Path(a.comments).read_text(encoding="utf8"), ns); COMMENTS = ns["COMMENTS"]

    zin = zipfile.ZipFile(a.src)
    root = etree.fromstring(zin.read("word/document.xml"))
    body = root.find(q("body"))
    rels = etree.fromstring(zin.read("word/_rels/document.xml.rels"))
    rid2target = {r.get("Id"): r.get("Target") for r in rels}

    media = {}
    for spec in a.replace:
        png, mname = spec.split("=")
        with Image.open(Path(a.figs) / png) as im:
            wpx, hpx = im.size
        done = False
        for blip in root.iter("{%s}blip" % NS["a"]):
            if rid2target.get(blip.get("{%s}embed" % NS["r"]), "").endswith("/" + mname):
                holder = blip
                while holder.tag not in ("{%s}inline" % NS["wp"], "{%s}anchor" % NS["wp"]):
                    holder = holder.getparent()
                ext = holder.find("{%s}extent" % NS["wp"]); cx = int(ext.get("cx")); cy = int(cx * hpx / wpx)
                ext.set("cy", str(cy))
                for e in holder.iter("{%s}ext" % NS["a"]):
                    e.set("cx", str(cx)); e.set("cy", str(cy))
                print(f"  {png} -> {mname}: {wpx}x{hpx}px, placed {cx/914400:.2f} x {cy/914400:.2f} in ({wpx/(cx/914400):.0f} ppi)")
                done = True
        assert done, mname
        media["word/media/" + mname] = (Path(a.figs) / png).read_bytes()

    for i, (pc, anchor, text) in enumerate(COMMENTS, 1):
        insert_after_text(find_para(body, pc), anchor, "[%s-%02d %s]" % (a.prefix, i, text))
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
