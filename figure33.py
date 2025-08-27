import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rows = [
    ("Insults", "Slight", 6),
    ("Insults", "Moderate", 3),
    ("Insults", "High", 4),
    ("Insults", "Extreme", 2),

    ("Personal Defamation", "Slight", 3),
    ("Personal Defamation", "Moderate", 3),
    ("Personal Defamation", "High", 4),
    ("Personal Defamation", "Extreme", 2),

    ("Threats", "Slight", 1),
    ("Threats", "Moderate", 2),
    ("Threats", "High", 2),
    ("Threats", "Extreme", 2),
    ("Threats", "None at all", 1),

    ("Sexism", "Slight", 1),    
    ("Sexism", "High", 2),
    ("Sexism", "Extreme", 2),

    ("Racism", "Slight", 1),
    ("Racism", "Moderate", 1),
    ("Racism", "High", 1),
    ("Racism", "Extreme", 1),

    ("Doxxing", "Extreme", 1),

    ("Other", "High", 1),
]

df = pd.DataFrame(rows, columns=["Category", "Severity", "Value"])

totals = df.groupby("Category")["Value"].sum().sort_values(ascending=False)
row_order = totals.index.tolist()
if "Insults" in row_order:
    row_order.remove("Insults")
    row_order = ["Insults"] + row_order
if "Other" in row_order:
    row_order.remove("Other")
    row_order = row_order + ["Other"]

colors = {
    "Extreme": "#1f4e79",
    "High": "#5b9bd5",
    "Moderate": "#d9d9d9",
    "Slight": "#f4b183",
    "None at all": "#a94438",
}

fig, ax = plt.subplots(figsize=(12, 6))

bar_h = 1.0         
category_gap = 10  

y_positions = []
bar_vals = []
bar_colors = []
cat_tick_pos = []
cat_tick_labels = []

y = 0.0
for cat in row_order:
    sub = df[df["Category"] == cat].copy()
    sub = sub[sub["Value"] > 0]             
    sub = sub.sort_values("Value", ascending=False)  

    if sub.empty:
        continue

    start_y = y
    for _, r in sub.iterrows():
        y_positions.append(y)
        bar_vals.append(r["Value"])
        bar_colors.append(colors.get(r["Severity"], "gray"))
        y += bar_h 
    
    mid = (start_y + y - bar_h) / 2.0
    cat_tick_pos.append(mid)
    cat_tick_labels.append(cat)

    y += category_gap  

ax.barh(y_positions, bar_vals, height=bar_h, color=bar_colors, edgecolor="none")

ax.set_yticks(cat_tick_pos)

ax.set_yticklabels(cat_tick_labels)
ax.invert_yaxis()                       
ax.tick_params(axis="y", length=0)      
ax.spines["left"].set_visible(True)   
ax.spines["right"].set_visible(False) 

ax.set_title("Forms Of Harassment Vs. Psychological Strain", fontsize=14, fontweight="bold", pad=14)
ax.set_xlabel("Frequency", fontweight="bold")
ax.set_ylabel("Form of Harassment", fontweight="bold")
ax.grid(axis="x", linestyle=":", linewidth=0.8, alpha=0.6)


max_x = int(max(bar_vals)) if bar_vals else 0
ax.set_xlim(0, max_x)
ax.set_xticks(np.arange(0, max_x + 1, 1))

present_sev = [s for s in colors if s in df["Severity"].unique()]
handles = [plt.Rectangle((0, 0), 1, 1, color=colors[s]) for s in present_sev]
ax.legend(handles, present_sev, title="Psychological Strain",
          loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=True)

plt.tight_layout()
plt.savefig("harassment_vs_strain_compact_groups.png", dpi=200)
plt.show()
