import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("primes.csv")

# Top 15, triées de la plus petite à la plus grande : barh empile les barres
# de bas en haut, donc pour avoir la plus grosse prime tout en haut, on
# trie en ordre croissant avant de tracer.
top15 = df.sort_values("prime", ascending=True).tail(15)

# --- Design ---
INK = "#0b0b0b"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BLUE = "#2a78d6"

plt.rcParams["font.family"] = "sans-serif"

fig, ax = plt.subplots(figsize=(10, 7))

bars = ax.barh(top15["nom"], top15["prime"], color=BLUE, height=0.65, zorder=3)

# Grille fine, seulement verticale (elle sert à lire les barres, pas les noms),
# placée derrière les barres (zorder plus bas).
ax.set_axisbelow(True)
ax.xaxis.grid(True, color=GRID, linewidth=1, zorder=0)
ax.yaxis.grid(False)

# On retire les bordures du cadre : seul l'axe bas reste, en gris discret.
for side in ("top", "right", "left"):
    ax.spines[side].set_visible(False)
ax.spines["bottom"].set_color("#c3c2b7")

ax.tick_params(axis="y", length=0, labelsize=11, colors=INK)
ax.tick_params(axis="x", length=0, labelsize=10, colors=INK_MUTED)
ax.set_xticks(ax.get_xticks())  # fige les ticks avant de les relabelliser
ax.set_xticklabels([f"{x / 1e9:.1f} Md" for x in ax.get_xticks()])

# Valeur affichée directement au bout de chaque barre : évite d'avoir à
# faire l'aller-retour avec l'axe pour lire la prime exacte.
for bar, valeur in zip(bars, top15["prime"]):
    ax.text(
        bar.get_width() + 0.05e9,
        bar.get_y() + bar.get_height() / 2,
        f"{valeur / 1e9:.2f} Md".replace(".", ","),
        va="center",
        fontsize=9.5,
        color=INK_MUTED,
    )

ax.set_xlim(0, top15["prime"].max() * 1.18)  # marge à droite pour les labels
ax.set_title(
    "Top 15 des primes les plus élevées de One Piece",
    fontsize=14,
    fontweight="bold",
    color=INK,
    loc="left",
    pad=16,
)

fig.tight_layout()
fig.savefig("top15_primes.png", dpi=150, facecolor="white")
print("Graphique enregistré : top15_primes.png")
