import csv 
import re 
import pandas as pd 
import sqlite3

# Importation des données brutes CSV
#On charge notre fichier de base 
#df = pd.read_csv('data/raw/rawdata.csv')

# Importation des données depuis la base sqlite3
bdd_path = 'data/raw/faostat_data.db'
conn = sqlite3.connect(bdd_path)
df = pd.read_sql_query("SELECT * FROM raw_data", conn)

#On supprime les colonnes inutiles
colonnes_drop = ["Element","Element Code","Domain","Domain Code"] 
df = df.drop(columns=colonnes_drop, errors='ignore')

# Suppression des lignes avec des valeurs manquantes dans la colonne "Value"
df = df.dropna(subset=["Value"])

#On standardise les noms de colonnes
df.columns = df.columns.str.lower().str.replace(' ', '_')

print(df.head())

#On va ensuite nettoyer les données avec du texte 
#On définit les colonnes textuelles à nettoyer
text_columns = ["area", "item", "unit"]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()  # supprimer espaces

#on cherche a extraire l'année au centre 
def extract_middle_year(s): 
    if len(s) == 9:
        start = int(s[2:4])
        end = int(s[6:])
        return 2000 + (start + end) // 2
    else :
        return s

# On applique les filtres de nettoyage sur le DataFrame
df["year"] = df["year"].apply(extract_middle_year)
df["item"] = df["item"].str.strip()
df["value"] = pd.to_numeric(df["value"].str.replace(',', '.') if df["value"].dtype == "object" else df["value"], errors='coerce')

# Sauvegarde des données nettoyées dans un fichier CSV
#df.to_csv('data/cleaned/clean_data.csv', index=False)

# Sauvegarde des données nettoyées dans une base sqlite3
df.to_sql('clean_data', conn, if_exists='replace', index=False)
conn.close()
