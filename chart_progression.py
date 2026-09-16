import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

df = pd.read_csv("progression.csv")

ordre_arcs = [
    "Passe", "East Blue", "Alabasta", "Enies Lobby", "Marineford",
    "Dressrosa", "Whole Cake Island", "Wano",
]
df["arc"] = pd.Categorical(df["arc"], categories=ordre_arcs, ordered=True)

large = df.pivot(index="arc", columns="personnage", values="prime").sort_index()
large = large.ffill()

# --- Design ---
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID = "#e1e0d9"
COULEURS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
            "#e87ba4", "#008300", "#4a3aa7", "#e34948"]

plt.rcParams["font.family"] = "sans-serif"

fig, ax = plt.subplots(figsize=(11, 7))

x = range(len(large.index))
positions_finales = []  # (personnage, x_index, valeur_reelle)

for i, personnage in enumerate(large.columns):
    couleur = COULEURS[i % len(COULEURS)]
    y = large[personnage]
    ax.plot(x, y, color=couleur, linewidth=2, marker="o", markersize=4, zorder=3)

    derniere_valeur = y.dropna().iloc[-1]
    derniere_position = y.last_valid_index()
    x_index = list(large.index).index(derniere_position)
    positions_finales.append([personnage, x_index, derniere_valeur])

ax.set_yscale("log")  # doit être posé avant de convertir en coordonnées écran

# --- Anti-collision des étiquettes, en pixels réels ---
# On convertit chaque point (valeur réelle, sur l'axe log) en position écran
# (transData), on écarte verticalement tout ce qui est à moins de
# `espacement_px` pixels du précédent, puis on reconvertit en coordonnées
# données (inverted) pour tracer les traits de rappel et les textes.
fig.canvas.draw()  # nécessaire pour que les transformations d'axes soient à jour
positions_finales.sort(key=lambda p: p[2])
espacement_px = 15

y_px_precedent = None
for entree in positions_finales:
    _, x_index, valeur_reelle = entree
    y_px = ax.transData.transform((x_index, valeur_reelle))[1]
    if y_px_precedent is not None:
        y_px = max(y_px, y_px_precedent + espacement_px)
    entree.append(y_px)
    y_px_precedent = y_px

for personnage, x_index, valeur_reelle, y_px_label in positions_finales:
    x_px = ax.transData.transform((x_index, valeur_reelle))[0]
    x_donnees_label, y_donnees_label = ax.transData.inverted().transform((x_px, y_px_label))

    if abs(y_px_label - ax.transData.transform((x_index, valeur_reelle))[1]) > 1:
        # L'étiquette a été décalée : un fin trait de rappel la relie à sa courbe.
        ax.plot(
            [x_index, x_index + 0.15], [valeur_reelle, y_donnees_label],
            color="#c3c2b7", linewidth=0.8, zorder=2,
        )
    ax.annotate(
        personnage,
        xy=(x_index + 0.15, y_donnees_label),
        xytext=(4, 0),
        textcoords="offset points",
        va="center",
        fontsize=9.5,
        color=INK_SECONDARY,
        fontweight="bold",
    )

ax.set_xticks(list(x))
ax.set_xticklabels(large.index, fontsize=10, color=INK_SECONDARY)

ax.set_axisbelow(True)
ax.yaxis.grid(True, which="major", color=GRID, linewidth=1, zorder=0)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.spines["left"].set_color("#c3c2b7")
ax.spines["bottom"].set_color("#c3c2b7")

# Ticks Y lisibles : "1 000", "1 M", "100 M", "1 Md" plutôt que 10^n.
def formatte_prime(valeur, _pos):
    if valeur >= 1e9:
        return f"{valeur / 1e9:g} Md"
    if valeur >= 1e6:
        return f"{valeur / 1e6:g} M"
    return f"{valeur:g}"

ax.yaxis.set_major_formatter(mticker.FuncFormatter(formatte_prime))
ax.tick_params(axis="y", length=0, labelsize=10, colors=INK_SECONDARY)
ax.tick_params(axis="x", length=0)

ax.set_xlim(-0.3, len(large.index) - 0.3 + 1.3)  # marge à droite pour les noms
ax.set_title(
    "Progression des primes des Chapeaux de Paille au fil de l'histoire",
    fontsize=14,
    fontweight="bold",
    color=INK,
    loc="left",
    pad=16,
)

fig.tight_layout()
fig.savefig("progression_primes.png", dpi=150, facecolor="white")
print("Graphique enregistré : progression_primes.png")
