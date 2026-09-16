import pandas as pd

df = pd.read_csv("progression.csv")

# L'ordre réel de l'histoire, pas l'ordre alphabétique.
ordre_arcs = [
    "Passe", "East Blue", "Alabasta", "Enies Lobby", "Marineford",
    "Dressrosa", "Whole Cake Island", "Wano",
]
df["arc"] = pd.Categorical(df["arc"], categories=ordre_arcs, ordered=True)

# Passage du format long (une ligne = un personnage + un arc) au format large
# (une colonne par personnage, une ligne par arc) : plus pratique pour tracer
# une courbe par personnage.
large = df.pivot(index="arc", columns="personnage", values="prime")
large = large.sort_index()

print("=== Avant ffill (les trous sont les arcs sans mise à jour) ===")
print(large)

# Propage la dernière prime connue de chaque personnage vers les arcs suivants.
large_rempli = large.ffill()

print("\n=== Après ffill ===")
print(large_rempli)

large_rempli.to_csv("progression_large.csv")
