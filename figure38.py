import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ===== Neue Daten: Countermeasures-Tabelle =====
counter_rows = [
    ("Community/PR support engaged", "Extreme", 0),
    ("Community/PR support engaged", "High",    2),
    ("Community/PR support engaged", "Moderate",2),
    ("Community/PR support engaged", "None at all", 0),
    ("Community/PR support engaged", "Slight",  5),

    ("Notifications turned off", "Extreme", 2),
    ("Notifications turned off", "High",    2),
    ("Notifications turned off", "Moderate",5),
    ("Notifications turned off", "None at all", 0),
    ("Notifications turned off", "Slight",  3),

    ("Other", "Extreme", 1),
    ("Other", "High",    1),
    ("Other", "Moderate",0),
    ("Other", "None at all", 0),
    ("Other", "Slight",  1),

    ("Posts moderated/deleted", "Extreme", 2),
    ("Posts moderated/deleted", "High",    2),
    ("Posts moderated/deleted", "Moderate",4),
    ("Posts moderated/deleted", "None at all", 1),
    ("Posts moderated/deleted", "Slight",  5),

    ("Self-care practices", "Extreme", 2),
    ("Self-care practices", "High",    3),
    ("Self-care practices", "Moderate",3),
    ("Self-care practices", "None at all", 0),
    ("Self-care practices", "Slight",  3),

    ("Social media break", "Extreme", 2),
    ("Social media break", "High",    3),
    ("Social media break", "Moderate",5),
    ("Social media break", "None at all", 0),
    ("Social media break", "Slight",  3),
]

# === DataFrame aufbauen (Spaltennamen an alten Code angelehnt)
df = pd.DataFrame(counter_rows, columns=["Channel", "Severity", "Value"])
df["Channel"]  = df["Channel"].astype(str).str.strip()
df["Severity"] = df["Severity"].astype(str).str.strip()
df["Value"]    = pd.to_numeric(df["Value"], errors="coerce").fillna(0).astype(int)

# 0-Werte auslassen (kein leerer Balken)
df = df[df["Value"] > 0].copy()

# === Farben (wie gehabt)
color_map = {
    "Extreme":     "#1f4e79",
    "High":        "#5b9bd5",
    "Moderate":    "#d9d9d9",
    "Slight":      "#f4b183",
    "None at all": "#a94438",
}

# === Countermeasures nach Gesamtsumme sortieren (absteigend)
totals = df.groupby("Channel")["Value"].sum().sort_values(ascending=False)
channels_sorted = totals.index.tolist()

# === Plot-Parameter
bar_w     = 0.22   # Breite einzelner Balken
group_gap = 0.75   # Abstand zwischen Gruppen
left_pad  = 0.60   # Abstand links zur Y-Achse

fig, ax = plt.subplots(figsize=(12, 6))

x_positions = []
x_ticklabels = []
bar_handles = {}
x_cursor = left_pad

for ch in channels_sorted:
    sub = df[df["Channel"] == ch].copy()
    # innerhalb der Maßnahme: Balken nach Häufigkeit absteigend
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

# === Achsen, Titel, Grid
ax.set_xticks(x_positions)
ax.set_xticklabels(x_ticklabels, rotation=35, ha="right")
ax.set_xlabel("Countermeasure", fontweight="bold")
ax.set_ylabel("Frequency", fontweight="bold")
ax.set_title("Countermeasures vs. Psychological Strain", fontweight="bold")

for label in ax.get_xticklabels():
    label.set_fontweight("bold")

ax.grid(axis="y", linestyle=":", linewidth=0.8, alpha=0.6)

# X-Limits passend zum Inhalt
ax.set_xlim(0, x_cursor - group_gap + left_pad)

# Y-Ticks in 1er-Schritten bis Maximum
ymax = int(df["Value"].max()) if not df.empty else 0
ax.set_yticks(np.arange(0, ymax + 1, 1))

# Legende in fixer Reihenfolge
legend_order = ["Extreme", "High", "Moderate", "Slight", "None at all"]
handles = [bar_handles[s] for s in legend_order if s in bar_handles]
labels  = [s for s in legend_order if s in bar_handles]
ax.legend(handles, labels, title="Psychological Strain", loc="center left", bbox_to_anchor=(1.02, 0.5))

plt.tight_layout()
plt.savefig("countermeasures_vs_strain_grouped.png", dpi=200)
plt.show()
