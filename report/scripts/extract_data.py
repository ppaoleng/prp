"""Extract experimental tables from the original DRAFT docx into tidy CSV files.
No numbers are retyped: every value is parsed from the source tables.
Source docx path is passed on the command line (original file is never modified)."""
import sys, re, csv, os
import docx
from docx.oxml.ns import qn
from docx.table import Table

SRC = sys.argv[1]
OUT = sys.argv[2]
ZW = "​"
d = docx.Document(SRC)

def cell_texts(tb):
    rows = []
    for r in tb.rows:
        seen, cells = None, []
        for c in r.cells:
            if c._tc is seen:  # merged horizontally
                continue
            seen = c._tc
            cells.append(c.text.replace(ZW, "").strip().replace("\n", " "))
        rows.append(cells)
    return rows

tables = [Table(t, d) for t in d.element.body.iterchildren(qn("w:tbl"))]
T = [cell_texts(t) for t in tables]
for i, t in enumerate(T):
    print(i, len(t), t[0][:3] if t else None)

def num(x):
    x = x.strip()
    if x in ("", "-", "–"):
        return None
    return float(x.replace(",", ""))

def write(name, header, rows):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", name, len(rows))

# ---- identify tables by header content ----
def find(pred):
    for i, t in enumerate(T):
        if pred(t):
            return i
    raise KeyError

i_mix   = find(lambda t: any("ส่วนผสมต้นแบบ" in " ".join(r) for r in t))
i_dens  = find(lambda t: "ความหนาแน่นเฉลี่ย" in " ".join(t[0]))
i_s1    = find(lambda t: t[0][:1]==["สูตรส่วนผสม"] and any("NA (อ้างอิง)" in r[0] for r in t) and len(t[1])>=6 and "ก้อนที่ 1" in " ".join(t[1]) and any(r[0].startswith("ไบโอชาร์") for r in t))
i_s2    = find(lambda t: any(r[0].startswith("RCA 0%") for r in t) and "ก้อนที่ 1" in " ".join(t[1]) and not any("%" in r[2] for r in t[2:3]) and "การดูดซึมน้ำ" not in " ".join(t[0]))
i_abs1  = find(lambda t: t[0][:2]==["อายุการบ่ม (วัน)","น้ำหนักเปียก (kg)"])
i_abs2  = find(lambda t: "การดูดซึมน้ำ (%)" in " ".join(t[0]) and any(r[0].startswith("RCA 0%") for r in t))
i_bpn   = find(lambda t: "BPN" in " ".join(t[0]))
i_mkt   = find(lambda t: "ผลตามเกณฑ์" in " ".join(t[0]))
i_a1    = find(lambda t: t[0][:3]==["สูตรส่วนผสม","อายุการบ่ม (วัน)","น้ำหนัก (kg)"])
i_a2    = find(lambda t: t[0][:2]==["ตัวอย่าง","ก้อนที่"] and "น้ำหนัก (kg)" in t[0])
i_a3    = find(lambda t: t[0][:2]==["สูตรส่วนผสม","ก้อนที่"] and "น้ำหนัก (kg)" in t[0])
print(dict(mix=i_mix,dens=i_dens,s1=i_s1,s2=i_s2,abs1=i_abs1,abs2=i_abs2,bpn=i_bpn,mkt=i_mkt,a1=i_a1,a2=i_a2,a3=i_a3))

# ---- Mix design (Table 3-1) ----
rows=[]; series=None
for r in T[i_mix][2:]:
    if len(r)==1 or (len(r)>=2 and r[0]==r[1] and len(set(r))==1):
        series = r[0]; continue
    if len(r)>=6:
        rows.append([series or "", r[0]] + [num(x) for x in r[1:6]])
write("mix_design_table3-1.csv",["series_note","mix","cement_g","sand_g","stone_g","rca_g","biochar_g"],rows)

# ---- strength tables ----
def parse_strength(t, label_col=0):
    out=[]; last=None
    for r in t[2:]:
        r=[x for x in r]
        if len(r)==6:
            mix,age,a,b,c,m = r; last=mix
        elif len(r)==5:
            mix=last; age,a,b,c,m = r
        else: continue
        out.append([mix,int(age),num(a),num(b),num(c),num(m)])
    return out
# Table 4-2 has merged mix cells: handle by carrying forward
def parse_merged(t):
    out=[]; last=None
    for r in t[2:]:
        if len(r)==6: last=r[0]; age,a,b,c,m=r[1:]
        elif len(r)==5: age,a,b,c,m=r
        else: continue
        out.append([last,int(age),num(a),num(b),num(c),num(m)])
    return out
write("strength_series1.csv",["mix","age_d","s1","s2","s3","mean_reported"],parse_merged(T[i_s1]))
write("strength_series2.csv",["mix","age_d","s1","s2","s3","mean_reported"],parse_merged(T[i_s2]))

# ---- density Table 4-1 ----
rows=[]
for r in T[i_dens][2:]:
    rows.append([r[0]]+[num(x) for x in r[1:5]])
write("density_table4-1.csv",["mix","d7","d14","d28","overall_reported"],rows)

# ---- absorption ----
rows=[]
for r in T[i_abs1][1:]:
    if r[0].isdigit(): rows.append(["Rab5%",int(r[0]),num(r[1]),num(r[2]),num(r[3])])
write("absorption_series1_rab5.csv",["mix","age_d","wet_kg","dry_kg","abs_pct"],rows)
rows=[]; last=None
for r in T[i_abs2][2:]:
    if len(r)==6: last=r[0]; age,a,b,c,m=r[1:]
    elif len(r)==5: age,a,b,c,m=r
    else: continue
    rows.append([last,int(age),num(a),num(b),num(c),num(m)])
write("absorption_series2.csv",["mix","age_d","s1","s2","s3","mean_reported"],rows)

# ---- existing BPN table (status: example/placeholder per user) ----
rows=[]; last=None
for r in T[i_bpn][1:]:
    if len(r)==6: last=r[0]; rows.append([r[0],r[1],int(r[2]),num(r[3]),num(r[4]),num(r[5])])
    elif len(r)==5: rows.append([last]+[r[0],int(r[1]),num(r[2]),num(r[3]),num(r[4])])
write("bpn_original_table4-6_EXAMPLE_VALUES.csv",["series","mix","age_d","bpn_dry","bpn_wet","diff"],rows)

# ---- market comparison Table 4-7 ----
rows=[]
for r in T[i_mkt][2:]:
    rows.append([r[0]]+[num(x) for x in r[1:5]]+[r[5]])
write("market_table4-7.csv",["sample","s1","s2","s3","mean_reported","tis_result_text"],rows)

# ---- Appendix A ----
rows=[]; last=None; lastage=None
for r in T[i_a1][1:]:
    mix,age,w,v,rho,m = r
    if mix: last=mix
    if age: lastage=int(age)
    rows.append([last,lastage,num(w),num(v),num(rho),num(m)])
write("appendixA1_density_per_specimen.csv",["mix","age_d","mass_kg","volume_m3","density","mean_reported"],rows)
rows=[]; last=None
for r in T[i_a2][1:]:
    s,n,w,f,m=r
    if s: last=s
    rows.append([last,int(n),num(w),num(f),num(m)])
write("appendixA2_market_per_specimen.csv",["sample","specimen","mass_kg","strength_MPa","mean_reported"],rows)
rows=[]; last=None
for r in T[i_a3][1:]:
    s,n,w,f,m=r
    if s: last=s
    rows.append([last,int(n),num(w),num(f),num(m)])
write("appendixA3_cube_per_specimen.csv",["mix","specimen","mass_kg","strength_MPa","mean_reported"],rows)
