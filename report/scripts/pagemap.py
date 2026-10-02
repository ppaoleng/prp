"""Compute body page numbers for TOC / list entries from a rendered PDF (via pdftotext).  Usage: pagemap.py file.pdf pages.json"""
import sys, os, re, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))

def norm(s):
    s = s.replace("<PH/>", "[PlaceHolder]"); s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"[\s​]+", "", s).replace("[PlaceHolder]", "PlaceHolder")

def main(pdf, out):
    items = json.load(open(os.path.join(HERE, "..", "data", "toc_items.json"), encoding="utf-8"))
    txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    pages = txt.split("\f")
    lines = [[norm(l) for l in p.split("\n") if l.strip()] for p in pages]
    # first body page = page with a line exactly "บทที่1" (own line) after the TOC pages
    start = next(i for i, ls in enumerate(lines) if "บทที่1" in ls)
    res = {}; cur = start; miss = []
    for kind, level, text in items:
        t = norm(text)
        key = t[:26]
        if kind == "h1" and text.startswith("บทที่"):
            num = re.match(r"บทที่ (\d+)", text).group(1)
            hit = next((i for i in range(cur, len(lines)) if f"บทที่{num}" in lines[i]), None)
        else:
            hit = next((i for i in range(cur, len(lines)) if any(l.startswith(key) for l in lines[i])), None)
        if hit is None:
            miss.append(text[:50]); continue
        cur = hit; res[text] = hit - start + 1
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("body starts at pdf page", start + 1, "| entries", len(res), "| missing", len(miss), miss[:10], "| total pages", len(pages) - 1)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
