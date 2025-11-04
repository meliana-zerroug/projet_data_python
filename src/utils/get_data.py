# Script pour récupérer des données FAOSTAT via faostat.get_data_df

import faostat

# Codes du jeu de données FAOSTAT 
dataset = 'FS'

# Définition des paramètres
# =======================

# Liste des codes de pays avec la norme UN M49
pays = None  # None pour tous les pays

# Liste des code des items :
#    - 21004  : '-- Prevalence of undernourishment (percent)',
#    - 21001  : '-- Number of people undernourished (million)',
#    - 21042  : '-- Number of obese adults (18 years and older) (million)',
#    - 210420 : '-- Prevalence of anemia among women of reproductive age (15-49 years) (percent)',
#    - 22013  : '-- Gross domestic product per capita, PPP, (constant 2021 international $)',
#    - 220001 : '-- Dietary energy supply used in the estimation of the prevalence of undernourishment (kcal/cap/day)',
#    - 21061  : '-- Average fat supply (g/cap/day) (3-year average)'

items = [21004, 21001, 21042, 210420, 22013, 220001, 21061]

# Code du type de valeur (Valeur approchée : 6120, Estimation haute et basse : 6210)
elements = [6120]

# Liste des codes des années sans prendre 2025 pour ne pas avoir de fausses données / mal insérées dans la base de données
annees = [i*10+3 for i in range(2000, 2024)] 

# Construction du dictionnaire de paramètres
params = {
    'area': pays,
    'item': items,
    'element': elements,
    'year3': annees
}

# =======================

# Récupération des données
try:
    df = faostat.get_data_df(dataset, pars=params)
    print(f"Données téléchargées : {df.shape[0]} lignes x {df.shape[1]} colonnes")
except Exception as e:
    print("Erreur lors du téléchargement :", e)

# Sauvegarde des données dans un fichier CSV dans le dossier data/raw
output_file = 'data/raw/faostat_data.csv'
df.to_csv(output_file, index=False)
print(f"Données sauvegardées dans : {output_file}")

