import pandas as pd

# Charge le CSV dans un DataFrame : une table en mémoire, comme une feuille Excel.
df = pd.read_csv("primes.csv")

print("=== Les 5 premières lignes ===")
print(df.head())

print("\n=== Structure du tableau (colonnes, types, valeurs manquantes) ===")
print(df.info())

print("\n=== Statistiques sur la colonne 'prime' ===")
print(df["prime"].describe())

print("\n=== Top 15 des plus grosses primes ===")
top15 = df.sort_values("prime", ascending=False).head(15)
print(top15[["nom", "equipage", "prime"]].to_string(index=False))
