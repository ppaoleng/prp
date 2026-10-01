import matplotlib.pyplot as plt
from fig_style import *
apply_style(); plt.rcParams["font.size"]=8.8
fig,(a,b)=plt.subplots(1,2,figsize=(7.0,3.3),gridspec_kw={"width_ratios":[1.45,1]})
x=[0,1]; w=0.5
mat=[920,1200]; lab=[6300,8800]; tot=[7220,10000]
a.bar(x,mat,w,color="white",edgecolor=INK,hatch="////",lw=0.9,label="Materials (manual) / filament + electricity (BIM-to-FDM)")
a.bar(x,lab,w,bottom=mat,color=[WARM,ACCENT],edgecolor=INK,lw=0.9)
from matplotlib.patches import Patch
for xi,m,l,t in zip(x,mat,lab,tot):
    a.text(xi,m+l/2,f"{l:,}",ha="center",va="center",color="white",fontweight="bold")
    a.text(xi+w/2+0.04,m/2,f"{m:,}",ha="left",va="center",color=INK_SEC,fontsize=8.8)
    a.text(xi,t+250,f"Total {t:,}",ha="center",va="bottom",fontweight="bold")
a.set_xticks(x); a.set_xticklabels(["Manual route\n(labour)","BIM-to-FDM route\n(printer service charge)"])
a.set_ylabel("Cost (THB)"); a.set_ylim(0,15200); a.set_xlim(-0.6,1.75)
a.yaxis.grid(True,color=GRID,lw=0.6); a.set_axisbelow(True)
a.legend(handles=[Patch(facecolor="white",edgecolor=INK,hatch="////",label="Materials / filament and electricity"),
  Patch(facecolor=WARM,edgecolor=INK,label="Labour (manual)"),Patch(facecolor=ACCENT,edgecolor=INK,label="Printer service charge")],
  loc="upper left",frameon=False,fontsize=7.8)
a.text(1,11900,"+2,780 THB (+38.5%)",ha="center",fontsize=8.8,color=RED)
a.set_title("(a) Cost breakdown",loc="left",fontweight="bold",fontsize=10)
b.bar(x,[6,3],w,color=[WARM,ACCENT],edgecolor=INK,lw=0.9)
for xi,v in zip(x,[6,3]): b.text(xi,v+0.12,f"{v} days",ha="center",fontweight="bold")
b.set_xticks(x); b.set_xticklabels(["Manual\nroute","BIM-to-FDM\nroute"]); b.set_ylim(0,7.5); b.set_xlim(-0.6,1.6)
b.set_ylabel("Fabrication duration (days)"); b.yaxis.grid(True,color=GRID,lw=0.6); b.set_axisbelow(True)
b.text(0.5,6.9,"−3 days (−50%)",ha="center",fontsize=8.8,color=RED)
b.set_title("(b) Duration",loc="left",fontweight="bold",fontsize=10)
fig.tight_layout(w_pad=2); save(fig,"fig6.png")
