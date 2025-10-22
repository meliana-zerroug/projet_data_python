import csv 
import re 
import pandas as pd 

#On charge notre fichier de base 
df = pd.read_csv('data/raw/rawdata.csv')

#On supprime les colonnes inutiles
colonnes_drop = ["Symbole","Description du Symbole","Domaine","Code Domaine"] 
df = df.drop(columns=colonnes_drop, errors='ignore')

#On standardise les noms de colonnes
df.columns = df.columns.str.lower().str.replace(' ', '_')


#On va ensuite nettoyer les données avec du texte 
#On définit les colonnes textuelles à nettoyer
text_columns = ["zone", "produit", "unité"]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()  # supprimer espaces
    df[col] = df[col].apply(lambda x: re.sub(r'[^\w\s]', ' ', x))  # supprimer caractères spéciaux on les remplace par rien

#on cherche a extraire l'année au centre 
def extract_middle_year(s): 
    if len(s) == 9:
        start = int(s[2:4])
        end = int(s[6:])
        return 2000 + (start + end) // 2
    else :
        return s

df["année"] = df["année"].apply(extract_middle_year)
df["valeur"] = pd.to_numeric(df["valeur"], errors='coerce')

df.to_csv('data/cleaned/clean_data.csv', index=False)
