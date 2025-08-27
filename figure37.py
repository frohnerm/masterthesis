import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rows = [
    ("Community/PR support engaged", 5, 4, 0),
    ("Notifications turned off",     5, 4, 3),
    ("Other",                        2, 0, 0),
    ("Posts moderated/deleted",      7, 3, 4),
    ("Self-care practices",          6, 3, 2),
    ("Social media break",           5, 5, 3),
]

df = pd.DataFrame(rows, columns=["Countermeasure", "25-34", "35-44", "45-54"]).set_index("Countermeasure")

col_sums = df.sum(axis=0).replace(0, np.nan)
df_pct = (df / col_sums) * 100
df_pct = df_pct.fillna(0)

age_groups = ["25-34", "35-44", "45-54"]

color_map = {
    "Community/PR support engaged": "#a94438",   # dunkelblau
    "Notifications turned off":     "#1f4e79",   # hellblau
    "Posts moderated/deleted":      "#5b9bd5",   # grau
    "Self-care practices":          "#f4b183",   # orange
    "Social media break":           "#d9d9d9",   # rotbraun
    "Other":                        "#4d4d4d",   # dunkelgrau
}

x = np.arange(len(age_groups))  
bar_w = 0.12

fig, ax = plt.subplots(figsize=(12, 6))

for j, age in enumerate(age_groups):    
    sub = df_pct[age].sort_values(ascending=True)
    offsets = (np.arange(len(sub)) - (len(sub)-1)/2) * bar_w
    for i, (cm, val) in enumerate(sub.items()):
        xpos = x[j] + offsets[i]
        ax.bar(xpos, val, width=bar_w, color=color_map.get(cm, "#999999"),
               label=cm if j == 0 else "")

ax.set_xticks(x)
ax.set_xticklabels(age_groups)
ax.set_xlabel("Age Group", fontweight="bold")
ax.set_ylabel("Percentage (%)", fontweight="bold")
ax.set_title("Countermeasures by Age Group (Normalised)", fontweight="bold")

for label in ax.get_xticklabels():
    label.set_fontweight("bold")

ymax = df_pct.max().max()
ax.set_ylim(0, ymax * 1.05)

ax.grid(False)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.legend(title="Countermeasure", title_fontproperties={"weight": "bold"}, loc="center left", bbox_to_anchor=(1.02, 0.5))

plt.tight_layout()
plt.show()
