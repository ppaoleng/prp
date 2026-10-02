import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "..", "figures"); OF = os.path.join(FIG, "orig")
_OT = json.load(open(os.path.join(HERE, "..", "data", "orig_text.json"), encoding="utf-8"))
def ot(i, repl=None):
    t = _OT[str(i)]
    for a, b in (repl or {}).items():
        assert a in t, (i, a)
        t = t.replace(a, b)
    return t
def fp(name): return os.path.join(FIG, name if name.endswith(".png") else name + ".png")
def op(name): return os.path.join(OF, name if name.endswith(".png") else name + ".png")
PH = "<PH/>"
def f1(x): return f"{x:.1f}"
def f2(x): return f"{x:.2f}"
def f0(x): return f"{x:,.0f}"
def pv(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}"
