import matplotlib as mpl, matplotlib.pyplot as plt
INK="#1a1a1a"; INK_SEC="#5c5c58"; ACCENT="#3d6a8a"; ACCENT_EDGE="#274a63"
WARM="#9c7a52"; WARM_EDGE="#6e5636"; GRID="#d9d9d4"; RED="#8a3b32"
def apply_style():
    mpl.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Liberation Sans","DejaVu Sans"],
      "font.size":9.6,"axes.edgecolor":INK,"axes.linewidth":0.9,"axes.labelcolor":INK,
      "xtick.color":INK,"ytick.color":INK,"text.color":INK,"axes.spines.top":False,"axes.spines.right":False,
      "hatch.linewidth":0.6})
def save(fig,path):
    fig.savefig(path,dpi=420,bbox_inches="tight",facecolor="white",pad_inches=0.08)
