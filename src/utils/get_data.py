# Script pour récupérer des données FAOSTAT via faostat.get_data_df

import faostat
import sqlite3
import pandas as pd
import requests

def get_data():
    """
    Récupère les données FAOSTAT et les sauvegarde dans une base de données sqlite3 locale
    """
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

    # ======================
    # Récupération des données de population totale depuis l'API de la Banque Mondiale
    # Paramètres
    indicator = "SP.POP.TOTL"
    date_range = "2000:2023"
    url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator}?date={date_range}&format=json&per_page=20000"

    # Requête
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()

    # On transforme en DataFrame
    df2 = pd.json_normalize(data[1])

    # Suppression des anciennes données et sauvegarde des nouvelles données brutes sur une base locale sqlite3
    bdd_path = 'data/faostat_data.db'
    conn = sqlite3.connect(bdd_path)
    df.to_sql('raw_data', conn, if_exists='replace', index=False)
    df2.to_sql('raw_pop_tot', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Données sauvegardées dans la base de données : {bdd_path}")

if __name__ == "__main__":
    get_data()