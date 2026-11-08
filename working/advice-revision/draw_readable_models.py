from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).parent
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':12})

def box(ax, xy, label, color='#E6EFF4', w=2.75, h=.9):
    x,y=xy
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.06',facecolor=color,edgecolor='#4C6474',lw=1.2))
    ax.text(x,y,label,ha='center',va='center',fontsize=11)

def arrow(ax, a, b, label='', rad=0, color='#45616D'):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=14,lw=1.4,color=color,connectionstyle=f'arc3,rad={rad}'))
    if label:
        x,y=(a[0]+b[0])/2,(a[1]+b[1])/2
        ax.text(x,y,label,ha='center',va='center',fontsize=10,color=color,bbox=dict(facecolor='white',edgecolor='none',pad=2))

# A readable extract: each arrow is an existing link or a collapsed path in v3.
fig,ax=plt.subplots(figsize=(8,7),layout='constrained')
ax.set(xlim=(0,12),ylim=(0,10));ax.axis('off')
ax.set_title('Selected feedback relationships in the model',loc='left',fontweight='bold',fontsize=16,pad=12)
pos={'stress':(2,8.7),'worry':(6,8.7),'spleen':(10,8.7),'sleep':(2,5.5),'heart':(6,5.5),'qi':(10,5.5),'fatigue':(2,2.2),'cooking':(6,2.2),'food':(10,2.2)}
labels={'stress':'Perceived stress','worry':'Sustained worry','spleen':'Spleen function\n(TCM)','qi':'Qi–blood\ngeneration (TCM)','heart':'Heart / Shen\nnourishment (TCM)','sleep':'Sleep quality','fatigue':'Fatigue','food':'Congee\nconsumption','cooking':'Cooking time /\npreparation demands'}
for k,xy in pos.items(): box(ax,xy,labels[k], '#FFF0D5' if k in ('spleen','qi','heart') else '#E6EFF4')
arrow(ax,(3.45,8.7),(4.55,8.7),'+')
arrow(ax,(7.45,8.7),(8.55,8.7),'−')
arrow(ax,(10,8.18),(10,6.02),'+')
arrow(ax,(8.55,5.5),(7.45,5.5),'+')
arrow(ax,(4.55,5.5),(3.45,5.5),'+')
arrow(ax,(2,4.98),(2,2.72),'−')
ax.plot([.55,.18,.18,.55],[2.2,2.2,8.7,8.7],color='#45616D',lw=1.4)
arrow(ax,(.18,8.7),(.55,8.7))
ax.text(.18,7.2,'+',ha='center',bbox=dict(facecolor='white',edgecolor='none',pad=1))
arrow(ax,(8.55,2.2),(7.45,2.2),'+')
arrow(ax,(5.4,2.72),(2.8,8.18),rad=-.06)
ax.text(4.25,3.6,'+ via time\npressure',ha='center',fontsize=9,bbox=dict(facecolor='white',edgecolor='none',pad=1))
ax.plot([11.45,11.8,11.8,11.45],[2.2,2.2,8.7,8.7],color='#B46E23',lw=1.4)
arrow(ax,(11.8,8.7),(11.45,8.7),color='#B46E23')
ax.text(11.8,7.2,'+',ha='center',color='#B46E23',bbox=dict(facecolor='white',edgecolor='none',pad=1))
arrow(ax,(9.25,2.72),(6.65,4.98),'+',color='#B46E23')
ax.text(6,.8,'+ = changes in the same direction     − = changes in opposite directions\nSome arrows combine intermediate steps for readability.',ha='center',va='center',fontsize=10)
fig.savefig(OUT/'readable_cld.png',dpi=230,facecolor='white')

fig,ax=plt.subplots(figsize=(8,7),layout='constrained')
ax.set(xlim=(0,12),ylim=(0,10));ax.axis('off')
ax.set_title('Selected changing states in the model',loc='left',fontweight='bold',fontsize=16,pad=12)
ax.text(6,9.15,'Each box represents a state that can build up or decline over time.',ha='center',fontsize=11)
rows=[(7.7,'Spleen function\n(TCM food transformation)','Nourishment','Depletion'),(4.9,'Calm Shen\n(TCM mental rest)','Settling','Disturbance'),(2.1,'Fatigue','Accumulation','Recovery')]
for y,title,left,right in rows:
    box(ax,(6,y),title,'#FFF0D5' if y>3 else '#E6EFF4',w=3.5,h=1.1)
    arrow(ax,(.9,y),(4.15,y))
    arrow(ax,(7.85,y),(11.1,y))
    ax.text(2.5,y+.38,left,ha='center',fontsize=11)
    ax.text(9.5,y+.38,right,ha='center',fontsize=11)
ax.text(2.5,6.65,'Food and congee\nadd nourishing support',ha='center',fontsize=10,color='#7E591D')
ax.text(9.5,6.65,'Worry, late nights and\nunhealthy habits add strain',ha='center',fontsize=10,color='#7E591D')
ax.text(2.5,3.85,'The recipe is assigned\na Shen-calming contribution',ha='center',fontsize=10,color='#7E591D')
ax.text(9.5,3.85,'Worry and disrupted routines\nadd disturbance',ha='center',fontsize=10,color='#7E591D')
ax.text(2.5,1.05,'Study and cooking demands\nadd to fatigue',ha='center',fontsize=10)
ax.text(9.5,1.05,'Sleep, nourishment and\nrecovery reduce fatigue',ha='center',fontsize=10)
ax.text(6,.25,'A simplified extract of the author’s model; other states and links are omitted.',ha='center',fontsize=10)
fig.savefig(OUT/'readable_sfd.png',dpi=230,facecolor='white')
print('Saved readable_cld.png and readable_sfd.png')
