import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from diag import *
from matplotlib.patches import Polygon, Circle, Wedge, Arc

rng = np.random.default_rng(11)

def particles(ax, x0, y0, w, h, n, r, hatch="//", fc="white", seed=1, avoid=None, ec=LINE, lw=0.6, zorder=3):
    g = np.random.default_rng(seed); pts = []
    tries = 0
    while len(pts) < n and tries < 4000:
        tries += 1
        x = g.uniform(x0 + r, x0 + w - r); y = g.uniform(y0 + r, y0 + h - r)
        if all((x - a) ** 2 + (y - b) ** 2 > (r + rr) ** 2 * 1.02 for a, b, rr in pts):
            pts.append((x, y, r))
    for x, y, rr in pts:
        ax.add_patch(Circle((x, y), rr, facecolor=fc, edgecolor=ec, lw=lw, hatch=hatch, zorder=zorder))
    return pts

def biochar_particle(ax, cx, cy, s=3.2, seed=3, pores=5, fc="#2b2b28", zorder=5):
    g = np.random.default_rng(seed)
    ang = np.sort(g.uniform(0, 2 * np.pi, 7)); rad = s * g.uniform(0.7, 1.15, 7)
    poly = np.c_[cx + rad * np.cos(ang), cy + rad * np.sin(ang)]
    ax.add_patch(Polygon(poly, closed=True, facecolor=fc, edgecolor=LINE, lw=0.6, zorder=zorder))
    for _ in range(pores):
        a = g.uniform(0, 2 * np.pi); rr = g.uniform(0, s * 0.55)
        ax.add_patch(Circle((cx + rr * np.cos(a), cy + rr * np.sin(a)), s * 0.11, facecolor="white", edgecolor="none", zorder=zorder + 1))

def mech():
    fig, ax = canvas(6.7, 5.4, 100, 80.6)
    # panel frames
    P = {"a": (1.5, 42, 47, 36), "b": (51.5, 42, 47, 36), "c": (1.5, 1.5, 47, 36), "d": (51.5, 1.5, 47, 36)}
    names = {"a": ("(a)  ผลของฟิลเลอร์และจุดนิวคลีเอชัน", "Low dose: filler and nucleation"), "b": ("(b)  การบ่มภายใน", "Internal curing by porous biochar"),
             "c": ("(c)  การเจือจางและความพรุน", "High dose: dilution and porosity"), "d": ("(d)  แนวโน้มเชิงแนวคิด", "Conceptual strength–dose response")}
    for k, (x, y, w, h) in P.items():
        ax.add_patch(Rectangle((x, y), w, h, facecolor="white", edgecolor=LINE, lw=0.8, zorder=1))
        label(ax, x + 1.5, y + h - 2.3, names[k][0], 6.9, "left", wt="bold"); label(ax, x + 1.5, y + h - 5.4, names[k][1], 5.6, "left", fam=EN, color=INK_SEC)
    # (a): cement grains (hatched circles) + small biochar particles between them
    x, y, w, h = P["a"]; pts = particles(ax, x + 2, y + 2, w - 4, h - 11, 14, 3.4, hatch="////", seed=2)
    g = np.random.default_rng(5)
    for i in range(7):
        px, py, _ = pts[i * 2 % len(pts)]; biochar_particle(ax, px + 3.4, py + 2.2, 1.2, seed=i, pores=1)
    label(ax, x + w / 2, y + 2.0, "ไฮเดรตเกิดบนผิวอนุภาค  →  โครงสร้างแน่นขึ้น", 5.8, color=INK_SEC, fam=THL) if False else label(ax, x + w / 2, y + 2.4, "อนุภาคละเอียดเป็นจุดเกาะของไฮเดรต โครงสร้างแน่นขึ้น", 5.7, color=INK_SEC, fam=THL)
    # (b): large porous biochar with water arrows
    x, y, w, h = P["b"]; biochar_particle(ax, x + w / 2, y + 17, 7.2, seed=9, pores=14)
    for a_ in np.linspace(0, 2 * np.pi, 9)[:-1]:
        arrow(ax, x + w / 2 + 7.7 * np.cos(a_), y + 17 + 7.7 * np.sin(a_), x + w / 2 + 13.5 * np.cos(a_), y + 17 + 12.5 * np.sin(a_), lw=0.7, ms=5, color=ACCENT_EDGE)
    label(ax, x + w / 2, y + 2.4, "น้ำที่ดูดซับไว้ปลดปล่อยช่วยการไฮเดรชันระยะหลัง", 5.7, color=INK_SEC, fam=THL)
    # (c): few cement grains, many voids
    x, y, w, h = P["c"]; pts = particles(ax, x + 2, y + 2, w - 4, h - 11, 6, 3.4, hatch="////", seed=4)
    for i in range(5): biochar_particle(ax, x + 6 + i * 8.5, y + 20 - (i % 2) * 8, 3.3, seed=20 + i, pores=4)
    for _ in range(7):
        vx, vy = rng.uniform(x + 3, x + w - 3), rng.uniform(y + 4, y + h - 12); ax.add_patch(Circle((vx, vy), 0.7, facecolor="white", edgecolor=LINE, lw=0.5, ls="--", zorder=6))
    label(ax, x + w / 2, y + 2.4, "ซีเมนต์น้อยลงและรูพรุนมากขึ้น กำลังลดลง", 5.7, color=INK_SEC, fam=THL)
    # (d): conceptual curve
    x, y, w, h = P["d"]
    X = np.linspace(0, 1, 100); Y = 0.55 + 0.9 * X * np.exp(-3.2 * X) * 3 - 0.6 * X
    ax2 = fig.add_axes([(x + 8) / 100, (y + 5) / 80.6, (w - 12) / 100, (h - 16) / 80.6])
    ax2.plot(X, Y, color=ACCENT_EDGE, lw=1.3); ax2.axhline(Y[0], color=INK_SEC, lw=0.7, ls=":")
    ax2.set_xticks([]); ax2.set_yticks([]); ax2.set_xlabel("biochar dose →", fontsize=6.3, labelpad=1); ax2.set_ylabel("strength →", fontsize=6.3, labelpad=1)
    for xx, t in ((0.12, "gain"), (0.42, "neutral"), (0.8, "loss")):
        ax2.text(xx, Y.min() - 0.04 if False else 0.3, t, fontsize=5.8, ha="center", color=INK_SEC)
    ax2.set_ylim(0.25, 1.5); ax2.spines[["top", "right"]].set_visible(False)
    save(fig, "s_biochar_mech")

def rca_structure():
    fig, ax = canvas(6.7, 3.9, 100, 58.2)
    ang = np.linspace(0, 2 * np.pi, 11)[:-1]; rad = 13 * np.array([1.0, 0.85, 1.1, 0.9, 1.05, 0.95, 1.1, 0.88, 1.0, 0.92])
    cx, cy = 30, 30
    def poly(scale):
        return np.c_[cx + scale * rad * np.cos(ang), cy + scale * rad * np.sin(ang)]
    def edge(scale, deg):
        a_ = np.radians(deg) % (2 * np.pi); r_ = np.interp(a_, np.r_[ang, 2 * np.pi], np.r_[rad, rad[0]]) * scale
        return cx + r_ * np.cos(a_), cy + r_ * np.sin(a_)
    ax.add_patch(Polygon(poly(2.05), closed=True, facecolor="white", edgecolor=LINE, lw=0.8, ls="--", zorder=1))            # new paste
    ax.add_patch(Polygon(poly(1.72), closed=True, facecolor="#d9d2c4", edgecolor=LINE, lw=0.6, hatch="xxxx", zorder=2))       # new ITZ band
    ax.add_patch(Polygon(poly(1.55), closed=True, facecolor="#e8e2d6", edgecolor=LINE, lw=0.8, hatch="..", zorder=3))         # adhered old mortar
    ax.add_patch(Polygon(poly(1.22), closed=True, facecolor="#c9c6bd", edgecolor=LINE, lw=0.6, hatch="xxxx", zorder=4))       # old ITZ band
    ax.add_patch(Polygon(poly(1.1), closed=True, facecolor="#9aa0a8", edgecolor=LINE, lw=0.8, hatch="////", zorder=5))        # original aggregate
    label(ax, cx, cy, "หินเดิม", 6.6, wt="bold"); ax.texts[-1].set_bbox(whitebox())
    def call(tx, ty, scale, deg, t, s):
        px, py = edge(scale, deg)
        ax.plot([px, tx], [py, ty], color=LINE, lw=0.6, zorder=8); ax.plot([px], [py], "o", color=LINE, ms=2.2, zorder=9)
        label(ax, tx + 1, ty, t, 6.2, "left", wt="bold"); label(ax, tx + 1, ty - 2.6, s, 5.4, "left", color=INK_SEC, fam=EN)
    call(62, 52, 1.95, 60, "ซีเมนต์เพสต์ใหม่", "new paste")
    call(62, 42, 1.64, 30, "ITZ ใหม่", "new ITZ  ~55\u201365 \u00b5m")
    call(62, 32, 1.38, 0, "มอร์ตาร์เดิมที่เกาะผิว", "adhered old mortar")
    call(62, 22, 1.16, -35, "ITZ เดิม", "old ITZ  ~40\u201350 \u00b5m")
    call(62, 12, 0.7, -65, "มวลรวมธรรมชาติเดิม", "original natural aggregate")
    ax.add_patch(Rectangle((62, 1), 36, 7.5, facecolor="#f4f2ec", edgecolor=LINE, lw=0.7, zorder=2))
    label(ax, 80, 4.8, "โมดูลัสนาโนอินเดนเทชัน: ITZ เดิม ≈ 70\u201380 %\nITZ ใหม่ ≈ 80\u201390 % ของเพสต์ข้างเคียง", 5.3, color=INK_SEC, fam=THL)
    save(fig, "s_rca_structure")

def slip_mech():
    fig, ax = canvas(6.7, 3.6, 100, 53.7)
    ax.add_patch(Rectangle((1.5, 4), 52, 47, facecolor="white", edgecolor=LINE, lw=0.8, zorder=1))
    label(ax, 3, 48.5, "(a)  กลไกแรงเสียดทานของยางสไลเดอร์", 6.9, "left", wt="bold")
    xs = np.linspace(5, 50, 500); prof = 9 + 1.5 * np.sin(xs * 0.55) + 0.8 * np.sin(xs * 2.7) + 0.4 * np.sin(xs * 9.1)
    ax.fill_between(xs, 5, prof, facecolor="#cfcbc0", edgecolor=LINE, lw=0.9, hatch="..", zorder=2)
    top = prof[(xs > 12) & (xs < 40)].max() + 0.4
    ax.add_patch(Rectangle((12, top), 28, 9, facecolor="#e1dfd6", edgecolor=LINE, lw=0.9, hatch="////", zorder=3))
    label(ax, 26, top + 4.5, "ยางสไลเดอร์ (rubber)", 6.0, bg=True)
    arrow(ax, 42, top + 4.5, 51, top + 4.5, lw=1.0); label(ax, 47, top + 7.4, "ทิศการเลื่อน", 5.4, color=INK_SEC, fam=THL)
    label(ax, 3.5, 41, "การสูญเสียพลังงานจากการเสียรูปของยาง (hysteresis)", 6.0, "left", wt="bold", color=WARM_EDGE)
    arrow(ax, 20, 39.2, 20, top + 7.0, lw=0.7, color=WARM_EDGE)
    label(ax, 3.5, 34.5, "การยึดเกาะที่ผิวสัมผัส (adhesion)", 6.0, "left", wt="bold", color=ACCENT_EDGE)
    arrow(ax, 33, 32.8, 33, top + 0.6, lw=0.7, color=ACCENT_EDGE)
    label(ax, 27.5, 6.8, "พื้นผิวบล็อก", 5.6, color=INK_SEC, fam=THL, bg=True)
    ax.add_patch(Rectangle((56.5, 4), 42, 47, facecolor="#f4f2ec", edgecolor=LINE, lw=0.8, zorder=1))
    label(ax, 58, 48.5, "(b)  ปัจจัยที่กำหนดค่า BPN ของบล็อก", 6.9, "left", wt="bold")
    items = [("ผิวหยาบละเอียด (microtexture)", "ความเหลี่ยมมุมของทราย/RCA · ความแข็งของแร่", 41.5), ("ผิวหยาบหยาบ (macrotexture)", "ลวดลายผิว · การระบายน้ำ", 33), ("วัสดุผสม", "ไบโอชาร์ (คาร์บอนอ่อน) · มอร์ตาร์เดิมของ RCA", 24.5), ("สภาพผิว", "แห้ง / เปียก · ฟิล์มน้ำ · ฝุ่นละเอียด", 16), ("อายุ/ความพรุน", "ไฮเดรชัน · การดูดซึมน้ำ", 8)]
    for t, s, y in items:
        box(ax, 58.5, y - 3.6, 38, 7.2, [L(t, 5.9, "bold"), L(s, 5.1, "normal", INK_SEC, THL)], fc="white", lw=0.6)
    save(fig, "s_slip_mech")

def pendulum():
    fig, ax = canvas(6.7, 3.9, 100, 58.2)
    px, py = 34, 50; L_ = 34
    ey = py - L_
    def pt(deg, r=L_): return px + r * np.cos(np.radians(deg)), py + r * np.sin(np.radians(deg))
    # release position (dotted), contact position (solid), follow-through (dotted grey)
    ex, ey2 = pt(-172); ax.plot([px, ex], [py, ey2], color=LINE, lw=0.9, ls=":", zorder=3); label(ax, ex - 1, ey2 + 3.2, "ตำแหน่งปล่อย", 5.8, "left", color=INK_SEC, fam=THL)
    ax.plot([px, px], [py, ey], color=LINE, lw=1.5, zorder=3)
    ex, ey3 = pt(-38); ax.plot([px, ex], [py, ey3], color=INK_SEC, lw=0.9, ls="--", zorder=2)
    ax.add_patch(Arc((px, py), 2 * L_, 2 * L_, theta1=-172, theta2=-38, color=INK_SEC, lw=0.6, ls="--", zorder=2))
    ax.add_patch(Rectangle((px - 3.6, ey - 1.2), 7.2, 3.6, facecolor="#e1dfd6", edgecolor=LINE, hatch="////", lw=0.8, zorder=5))
    ax.add_patch(Rectangle((4, ey - 5.2), 58, 4, facecolor="#cfcbc0", edgecolor=LINE, hatch="..", lw=0.8, zorder=2))
    label(ax, 7, ey - 7.6, "ตัวอย่างบล็อกปูพื้น (ผิวหน้า)", 6.0, "left", color=INK_SEC, fam=THL)
    arrow(ax, px - 6.3, ey - 11.2, px + 6.3, ey - 11.2, lw=0.8, style="<|-|>", ms=6); label(ax, px, ey - 13.6, "ระยะสัมผัส 12.5 ซม. (ตามร่าง)", 5.6, color=INK_SEC, fam=THL)
    ax.add_patch(Circle((px, py), 1.0, facecolor=LINE, zorder=6)); label(ax, px, py + 3.2, "จุดหมุน", 5.8, color=INK_SEC, fam=THL)
    # scale on the follow-through side
    ax.add_patch(Wedge((px, py), 15, -78, -22, width=0.9, facecolor="white", edgecolor=LINE, lw=0.8, zorder=4))
    for a in np.linspace(-77, -23, 10):
        ax.plot([px + 13.4 * np.cos(np.radians(a)), px + 15 * np.cos(np.radians(a))], [py + 13.4 * np.sin(np.radians(a)), py + 15 * np.sin(np.radians(a))], color=LINE, lw=0.6, zorder=5)
    arrow(ax, px, py, px + 13 * np.cos(np.radians(-48)), py + 13 * np.sin(np.radians(-48)), lw=0.9, ms=6)
    label(ax, px + 17.5, py - 9.0, "เข็มอ่านค่า BPN", 5.8, "left", wt="bold")
    ax.add_patch(Rectangle((66, 12), 32, 41, facecolor="#f4f2ec", edgecolor=LINE, lw=0.8, zorder=1))
    label(ax, 68, 49.8, "ขั้นตอนการวัด", 6.8, "left", wt="bold")
    for i, t in enumerate(["1. ปรับระดับและตั้งศูนย์", "2. ตั้งระยะสัมผัสของสไลเดอร์", "3. วัดอุณหภูมิผิว", "4. แห้ง: ปล่อย 3 ครั้ง", "5. เปียก: พรมน้ำทุกครั้ง", "6. เฉลี่ยเป็น BPN"]):
        label(ax, 68, 44.2 - i * 5.2, t, 5.9, "left", color=INK, fam=THL)
    save(fig, "s_pendulum")

if __name__ == "__main__":
    mech(); rca_structure(); slip_mech(); pendulum()
