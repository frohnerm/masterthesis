import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rows = ["None at all", "Slight", "Moderate", "High", "Extreme"]
cols = ["None at all", "Slight", "Moderate", "High", "Extreme"]

data = [
    [1, 0, 0, 0, 0],  # None at all
    [3, 2, 1, 0, 0],  # Slight
    [0, 3, 2, 0, 0],  # Moderate
    [0, 0, 1, 4, 0],  # High
    [0, 0, 0, 1, 1],  # Extreme
]

df = pd.DataFrame(data, index=rows, columns=cols)

row_sums = df.sum(axis=1).replace(0, np.nan)
df_norm = (df.T / row_sums).T.fillna(0)

impact_order = ["None at all", "Slight", "Moderate", "High", "Extreme"]

color_map = {
    "Extreme":      "#1f4e79",
    "High":         "#5b9bd5",
    "Moderate":     "#d9d9d9",
    "Slight":       "#f4b183",
    "None at all":  "#a94438",
}
colors = [color_map[c] for c in reversed(impact_order)]

x = np.arange(len(df_norm.index))
bar_w = 0.16
fig, ax = plt.subplots(figsize=(10, 5))

for i, impact in enumerate(impact_order):
    ax.bar(x + i*bar_w, df_norm[impact].values * 100, width=bar_w,
           label=impact, color=colors[i])

ax.set_xticks(x + bar_w*2)
ax.set_xticklabels(df_norm.index, rotation=0)
ax.set_xlabel("Psychological Strain", fontweight="bold")
ax.set_ylabel("Frequency (%)", fontweight="bold")
ax.set_title("Psychological Strain vs. Productivity/Creativity (Normalised)", fontweight="bold")

ax.set_ylim(0, 100)
ax.set_yticks(np.arange(0, 101, 20))

ax.grid(axis="y", linestyle=":", linewidth=0.8, alpha=0.6)

ax.spines["top"].set_visible(False)

ax.legend(title="Impact on Productivity/Creativity", loc="center left", bbox_to_anchor=(1.02, 0.5))

plt.tight_layout()
plt.show()

