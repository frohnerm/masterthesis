import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

rows = [
    ("Instagram", "Slight", 2),
    ("Instagram", "Moderate", 1),
    ("Instagram", "High", 1),
    ("Instagram", "Extreme", 1),

    ("Reddit", "Slight", 3),
    ("Reddit", "Moderate", 2),
    ("Reddit", "High", 1),
    ("Reddit", "Extreme", 1),

    ("Steam", "Slight", 4),
    ("Steam", "Moderate", 4),
    ("Steam", "High", 3),   

    ("E-Mail", "Slight", 2),
    ("E-Mail", "Moderate", 2),
    ("E-Mail", "High", 1),
    ("E-Mail", "Extreme", 2),

    ("Other", "High", 1),
    ("Other", "Extreme", 1),
    ("Other", "Moderate", 1),
    ("Other", "None at all", 1),

    ("4chan", "Extreme", 1),

    ("TikTok", "Slight", 3),
    ("TikTok", "Moderate", 1),   
    ("TikTok", "Extreme", 1),
    
    ("Twitch", "Moderate", 2),
    ("Twitch", "High", 1),    

    ("Discord", "Slight", 5),
    ("Discord", "Moderate", 2),
    ("Discord", "High", 1),
    ("Discord", "Extreme", 1),

    ("Facebook", "Slight", 1),
    ("Facebook", "Moderate", 1),
    ("Facebook", "High", 1),    

    ("Twitter/X", "Slight", 2),
    ("Twitter/X", "Moderate", 2),
    ("Twitter/X", "High", 3),
    ("Twitter/X", "Extreme", 1),
]

df = pd.DataFrame(rows, columns=["Channel", "Severity", "Value"])
df["Channel"] = df["Channel"].astype(str).str.strip()
df["Severity"] = df["Severity"].astype(str).str.strip()
df["Value"]   = pd.to_numeric(df["Value"], errors="coerce").fillna(0).astype(int)

df = df[df["Value"] > 0].copy()


color_map = {
    "Extreme":  "#1f4e79",
    "High":     "#5b9bd5",
    "Moderate": "#d9d9d9",
    "Slight":   "#f4b183",
    "None at all": "#a94438",  
}

totals = df.groupby("Channel")["Value"].sum().sort_values(ascending=False)
channels_sorted = totals.index.tolist()

priority_first = ["Discord"]
channels_sorted = [c for c in priority_first if c in channels_sorted] + \
                  [c for c in channels_sorted if c not in priority_first]

bar_w     = 0.22  
group_gap = 0.75   
left_pad  = 0.60   

fig, ax = plt.subplots(figsize=(12, 6))

x_positions = []  
x_ticklabels = []
bar_handles = {}  

x_cursor = left_pad

for ch in channels_sorted:
    sub = df[df["Channel"] == ch].copy()  
    sub = sub.sort_values("Value", ascending=False)

    n = len(sub)
    group_width = max(n * bar_w, bar_w)
    start = x_cursor - group_width/2 + bar_w/2

    for i, row in enumerate(sub.itertuples(index=False)):
        x = start + i * bar_w
        h = ax.bar(
            x, row.Value, width=bar_w,
            color=color_map.get(row.Severity, "#999999"),
            edgecolor="none", label=row.Severity
        )
        if row.Severity not in bar_handles:
            bar_handles[row.Severity] = h

    x_positions.append(x_cursor)
    x_ticklabels.append(ch)

    x_cursor += group_width + group_gap

ax.set_xticks(x_positions)
ax.set_xticklabels(x_ticklabels, rotation=45, ha="right")
ax.set_xlabel("Channel")
ax.set_ylabel("Frequency")
ax.set_title("Channels vs Reporting/Moderating Tools")

ax.grid(axis="y", linestyle=":", linewidth=0.8, alpha=0.6)

ax.set_xlim(0, x_cursor - group_gap + left_pad)

ymax = int(df["Value"].max()) if not df.empty else 0
ax.set_yticks(np.arange(0, ymax + 1, 1))

legend_order = ["Extreme", "High", "Moderate", "Slight", "None at all"]
handles = [bar_handles[s] for s in legend_order if s in bar_handles]
labels  = [s for s in legend_order if s in bar_handles]
ax.legend(handles, labels, title="Severity", loc="center left", bbox_to_anchor=(1.02, 0.5))

plt.tight_layout()
plt.savefig("channels_vs_tools_grouped_sorted.png", dpi=200)
plt.show()
