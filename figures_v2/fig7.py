import numpy as np, matplotlib.pyplot as plt
from fig_style import *
apply_style(); plt.rcParams["font.size"]=8.4
m=920; n=3; d=6; f=1200; s=8800; w=350; TM=6; TP=3
CM=lambda w: m+n*d*w
fig,ax=plt.subplots(1,3,figsize=(7.4,3.0))
a=ax[0]; S=np.linspace(0,10000,50); a.plot(S,f+S-CM(w),color=ACCENT,lw=1.6)
a.axhline(0,color=INK_SEC,lw=0.8,ls="--"); a.plot([8800],[2780],"o",ms=4.5,color=RED,zorder=5); a.plot([6020],[0],"s",ms=4.5,color=INK,zorder=5)
a.annotate("recorded: 8,800 THB\n(+2,780)",xy=(8800,2780),xytext=(4300,3700),fontsize=7.4,color=RED,arrowprops=dict(arrowstyle="-",color=RED,lw=0.7))
a.annotate("parity: 6,020 THB\n(−31.6%)",xy=(6020,0),xytext=(700,2300),fontsize=7.4,arrowprops=dict(arrowstyle="-",color=INK,lw=0.7))
a.set_xlabel("Printer service charge (THB)"); a.set_ylabel("Printing minus manual cost (THB)"); a.set_title("(a)",loc="left",fontweight="bold")
b=ax[1]; W=np.linspace(250,600,50); b.plot(W,10000-CM(W),color=WARM,lw=1.6); b.axhline(0,color=INK_SEC,lw=0.8,ls="--")
b.plot([350],[2780],"o",ms=4.5,color=RED,zorder=5); b.plot([300],[3680],"o",ms=4.5,color=WARM_EDGE,zorder=5); b.plot([504.4],[0],"s",ms=4.5,color=INK,zorder=5)
b.annotate("350 THB: +2,780",xy=(350,2780),xytext=(400,3500),fontsize=7.4,color=RED,arrowprops=dict(arrowstyle="-",color=RED,lw=0.7))
b.annotate("300 THB: +3,680",xy=(300,3680),xytext=(325,4700),fontsize=7.4,color=WARM_EDGE,arrowprops=dict(arrowstyle="-",color=WARM_EDGE,lw=0.7))
b.annotate("parity: ≈504 THB",xy=(504.4,0),xytext=(410,-1500),fontsize=7.4,arrowprops=dict(arrowstyle="-",color=INK,lw=0.7))
b.set_ylim(-2300,5600)
b.set_xlabel("Daily wage per person (THB)"); b.set_ylabel("Printing minus manual cost (THB)"); b.set_title("(b)",loc="left",fontweight="bold")
c=ax[2]; t=np.array([0,.5,1,1.5,2]); r=(TM-TP-t)/TM*100
c.axvspan(1,2,facecolor="#ece8dc",edgecolor="none",zorder=0)
c.plot(t,r,"-o",color=ACCENT,lw=1.6,ms=5)
for ti,ri in zip(t,r): c.text(ti+0.07,ri+2.6,f"{ri:.1f}%",ha="left",fontsize=7.4,zorder=6)
c.text(1.5,5,"reported Revit\nmodelling: 1–2 days",ha="center",fontsize=7.4,zorder=6)
c.set_ylim(0,62); c.set_xlabel("Added Revit modelling time (days)"); c.set_ylabel("Duration reduction vs. manual (%)"); c.set_title("(c)",loc="left",fontweight="bold")
for x_ in ax: x_.grid(True,color=GRID,lw=0.5); x_.set_axisbelow(True)
fig.tight_layout(w_pad=1.6); save(fig,"fig7.png")
