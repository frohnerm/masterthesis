import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rows = [
    ("Instagram", "Slightly helpful", 2),
    ("Instagram", "Moderately helpful", 2),
    ("Instagram", "Very helpful", 0),
    ("Instagram", "Not helpful at all", 1),

    ("Reddit", "Slightly helpful", 4),
    ("Reddit", "Moderately helpful", 2),
    ("Reddit", "Very helpful", 0),
    ("Reddit", "Not helpful at all", 1),

    ("Steam", "Slightly helpful", 4),
    ("Steam", "Moderately helpful", 3),
    ("Steam", "Very helpful", 1),
    ("Steam", "Not helpful at all", 2),

    ("E-Mail", "Slightly helpful", 4),
    ("E-Mail", "Moderately helpful", 1),
    ("E-Mail", "Very helpful", 1),
    ("E-Mail", "Not helpful at all", 1),

    ("Other", "Slightly helpful", 1),
    ("Other", "Moderately helpful", 2),
    ("Other", "Very helpful", 0),
    ("Other", "Not helpful at all", 1),

    ("4chan", "Slightly helpful", 0),
    ("4chan", "Moderately helpful", 0),
    ("4chan", "Very helpful", 0),
    ("4chan", "Not helpful at all", 0),

    ("TikTok", "Slightly helpful", 2),
    ("TikTok", "Moderately helpful", 3),
    ("TikTok", "Very helpful", 0),
    ("TikTok", "Not helpful at all", 0),

    ("Twitch", "Slightly helpful", 3),
    ("Twitch", "Moderately helpful", 1),
    ("Twitch", "Very helpful", 0),
    ("Twitch", "Not helpful at all", 0),

    ("Discord", "Slightly helpful", 2),
    ("Discord", "Moderately helpful", 3),
    ("Discord", "Very helpful", 1),
    ("Discord", "Not helpful at all", 3),

    ("Facebook", "Slightly helpful", 1),
    ("Facebook", "Moderately helpful", 0),
    ("Facebook", "Very helpful", 0),
    ("Facebook", "Not helpful at all", 2),

    ("Twitter/X", "Slightly helpful", 4),
    ("Twitter/X", "Moderately helpful", 3),
    ("Twitter/X", "Very helpful", 0),
    ("Twitter/X", "Not helpful at all", 1),
]

df = pd.DataFrame(rows, columns=["Channel", "Helpfulness", "Value"])
totals = df.groupby("Channel")["Value"].sum().sort_values(ascending=False)
row_order = totals.index.tolist()

fig, ax = plt.subplots(figsize=(12, 6))

color_map = {
    "Very helpful": "#1f4e79",
    "Moderately helpful": "#5b9bd5",
    "Slightly helpful": "#f4b183",
    "Not helpful at all": "#a94438",
}

bar_h = 2      
category_gap = 10 

y_positions, bar_vals, bar_colors = [], [], []
cat_tick_pos, cat_tick_labels = [], []

y = 0.0
for ch in row_order:
    sub = df[df["Channel"] == ch].copy()
    sub = sub[sub["Value"] > 0]
    sub = sub.sort_values("Value", ascending=False)

    if sub.empty:
        continue

    start_y = y
    for _, r in sub.iterrows():
        y_positions.append(y)
        bar_vals.append(int(r["Value"]))
        bar_colors.append(color_map.get(r["Helpfulness"], "gray"))
        y += bar_h
  
    mid = (start_y + y - bar_h) / 2.0
    cat_tick_pos.append(mid)
    cat_tick_labels.append(ch)

    y += category_gap

ax.barh(y_positions, bar_vals, height=bar_h, color=bar_colors, edgecolor="none")

ax.set_yticks(cat_tick_pos)
ax.set_yticklabels(cat_tick_labels)
ax.invert_yaxis()
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(True)
ax.spines["right"].set_visible(False)

ax.set_title("Channels vs Reporting/Moderating Tools", fontsize=14, fontweight="bold", pad=14)
ax.set_xlabel("Frequency", fontweight="bold")
ax.set_ylabel("Channel", fontweight="bold")
ax.grid(axis="x", linestyle=":", linewidth=0.8, alpha=0.6)

max_x = int(max(bar_vals)) if bar_vals else 0
ax.set_xlim(0, max_x)
ax.set_xticks(np.arange(0, max_x + 1, 1))

present = [k for k in color_map if k in df["Helpfulness"].unique()]
handles = [plt.Rectangle((0,0), 1, 1, color=color_map[k]) for k in present]
ax.legend(handles, present, title="Helpfulness",
          loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=True)

plt.tight_layout()
plt.savefig("channels_vs_tools.png", dpi=200)
plt.show()
