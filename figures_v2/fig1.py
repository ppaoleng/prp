import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
from fig_style import *
apply_style()
fig,ax=plt.subplots(figsize=(7.6,5.9)); ax.set_xlim(0,100); ax.set_ylim(-14,70); ax.axis("off")
def box(x,y,w,h,txt,fc="white",ec=INK,tc=INK,bold=False,fs=8.8):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=0.9)); ax.text(x+w/2,y+h/2,txt,ha="center",va="center",color=tc,fontsize=fs,fontweight="bold" if bold else "normal",linespacing=1.3)
def arr(x1,y1,x2,y2,c=INK):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=9,lw=0.9,color=c,shrinkA=0,shrinkB=0))
box(8,61,84,8,"Case: two-storey reinforced-concrete house, 3 bedrooms, 3 bathrooms,\napprox. 315 m² usable area; physical model at 1:60",fc="#ececE8",bold=True,fs=8.4)
box(2,50,46,6.5,"Route A  BIM-to-FDM printing",fc=ACCENT,ec=ACCENT_EDGE,tc="white",bold=True,fs=9.6)
box(52,50,46,6.5,"Route B  Manual fabrication (baseline)",fc=WARM,ec=WARM_EDGE,tc="white",bold=True,fs=9.6)
arr(35,61,25,56.5); arr(65,61,75,56.5)
A=["A1  BIM modelling in Autodesk Revit\ngrids, levels, floors, walls, roof\n(1–2 days reported; not in baseline)","A2  Export to STL (binary)\nFile > Export > CAD Formats > STL","A3  Slicing in Ultimaker Cura\n(screenshot: Ender-3 profile, PLA,\n0.2 mm layer, 20% infill)","A4  FDM printing in separate parts\nfloors, walls, stairs, roof (3 days);\nglued onto printed base"]
B=["B1  2D plans scaled to 1:60,\nprinted as cutting templates","B2  Templates pasted on Plaswood\nsheets; clear PVC for glazing","B3  Hand cutting (cutter, steel ruler, mat);\nlaser cutting suggested for small railings","B4  Gluing and assembly\n(3 persons, 6 days)"]
hs=[9.5,7.5,9.5,9.5]; hb=[7.5,7.5,7.5,7.5]
y=46
for i,(t,h) in enumerate(zip(A,hs)):
    y-=h; box(2,y,46,h,t,ec=ACCENT_EDGE); 
    if i<3: arr(25,y,25,y-2.2,ACCENT_EDGE)
    y-=2.2
yb=46
for i,(t,h) in enumerate(zip(B,hb)):
    yb-=h; box(52,yb,46,h,t,ec=WARM_EDGE)
    if i<3: arr(75,yb,75,yb-2.2,WARM_EDGE)
    yb-=2.2
box(6,-11,88,6.5,"Accounting: materials | labour or printer service charge | duration  →  sensitivity analysis",fc="#ececE8",bold=True,fs=8.4)
arr(25,y+2.2-0.1,25,-4.5,INK); arr(75,yb+2.2-0.1,75,-4.5,INK)
save(fig,"fig1.png")
