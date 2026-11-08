import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[2]
data = json.loads((root / 'Model Simulation/05_Model_v3_holistic/3_Simulation_Charts/summary_v3.json').read_text())
scenarios = list(data['scenarios'].values())
physical = [s['Physical_Wellbeing']['semester_mean'] for s in scenarios]
mental = [s['Mental_Wellbeing']['semester_mean'] for s in scenarios]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
fig, ax = plt.subplots(figsize=(8.2, 4.8), layout='constrained')
x = np.arange(4)
for offset, vals, color, label in [(-.18, physical, '#315B80', 'Physical wellbeing'), (.18, mental, '#4D927F', 'Mental wellbeing')]:
    bars = ax.bar(x + offset, vals, .34, color=color, label=label)
    ax.bar_label(bars, labels=[f'{v:.1f}' for v in vals], padding=4, fontsize=10)
ax.set_ylim(0, 100)
ax.set_ylabel('Simulated score (0–100)')
ax.set_xticks(x, ['S1\nUnhealthy habits\nNo congee', 'S2\nHealthier routines\nNo congee', 'S3\nHealthier routines\n2 portions/week', 'S4\nHealthier routines\n7 portions/week'])
ax.set_title('Lifestyle and congee in the model', loc='left', fontsize=15, fontweight='bold', pad=14)
ax.legend(loc='upper left', ncol=2, frameon=False, bbox_to_anchor=(0, 1.02))
ax.grid(axis='y', color='#DDE2E6', linewidth=.7)
ax.set_axisbelow(True)
for side in ['top', 'right']:
    ax.spines[side].set_visible(False)
ax.spines['left'].set_color('#A0A8AF')
ax.spines['bottom'].set_color('#A0A8AF')
fig.savefig(Path(__file__).with_name('scenario_comparison.png'), dpi=240, facecolor='white')
print('Source: summary_v3.json; median of 1,000 profiles’ weeks 1–17 average scores.')
print('Saved scenario_comparison.png')
