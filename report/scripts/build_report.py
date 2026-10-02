"""Build the improved report (v2).  Usage:  python3 build_report.py [--pages pages.json] [--out file.docx]
Two passes: a dry pass collects figure/table/equation labels, then a render pass resolves every {fig:..}/{tab:..}/{eq:..}/{c:..} marker.
The original draft is never modified; the new file is written to report/output/."""
import os, sys, json, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import docx_builder as D
import rnum, front, ch1, ch2a, ch2b, ch3, ch4a, ch4b, ch4c, ch5, back

ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "source_original", "2.PRP_รายงานฉบับสมบูรณ์ 2569 [DRAFT].docx")
OUT = os.path.join(ROOT, "output", "PRP_รายงานฉบับสมบูรณ์_2569_v2.docx")
BODY = (ch1, ch2a, ch2b, ch3, ch4a, ch4b, ch4c, ch5, back)


def run(pages=None, out=OUT):
    N = rnum.load()
    reg0 = D.Registry(); b0 = D.Builder(SRC, reg0, dry=True)
    front.build(b0, N)
    for m in BODY: m.build(b0, N)
    reg = D.Registry(); reg.labels = reg0.labels
    b = D.Builder(SRC, reg, dry=False)
    markers = front.build(b, N)
    for m in BODY: m.build(b, N)
    front.finish(b, markers, pages or {})
    b.set_update_fields()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    b.save(out)
    info = dict(missing=sorted(reg.missing), n_cites=len(reg.cites), labels={k: len(v) for k, v in reg.labels.items()}, toc=[(k, l, t) for k, l, t, _ in b.toc_items])
    return info


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--pages"); ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    pages = json.load(open(a.pages, encoding="utf-8")) if a.pages and os.path.exists(a.pages) else {}
    info = run(pages, a.out)
    print("missing refs:", info["missing"]); print("citations:", info["n_cites"], "labels:", info["labels"])
    json.dump(info["toc"], open(os.path.join(HERE, "..", "data", "toc_items.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("saved", a.out)
