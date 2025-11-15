from src.utils.get_data import get_data
import pandas as pd 
import sqlite3

def clean_data():
    """
    Nettoie les données brutes téléchargées et les sauvegarde dans une base de données sqlite3
    """ 
    # Conexion à la base de données
    bdd_path = 'faostat_data.db'
    conn = sqlite3.connect(bdd_path)

    # Vérification de l'existence des tables raw_data et raw_pop_tot
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    trouvees = {row[0] for row in cur.fetchall()}
    if 'raw_data' not in trouvees or 'raw_pop_tot' not in trouvees:
        get_data()

    # Importation des données depuis la base sqlite3
    df = pd.read_sql_query("SELECT * FROM raw_data", conn)
    df_pop = pd.read_sql_query("SELECT * FROM raw_pop_tot", conn)

    # On supprime les colonnes inutiles
    colonnes_drop = ["Element","Element Code","Domain","Domain Code"] 
    df = df.drop(columns=colonnes_drop, errors='ignore')

    # Suppression des lignes avec des valeurs manquantes dans la colonne "Value"
    df = df.dropna(subset=["Value"])

    #On standardise les noms de colonnes
    df.columns = df.columns.str.lower().str.replace(' ', '_')

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
    df["value"] = pd.to_numeric(df["value"].str.replace(',', '.').replace('<', '') if df["value"].dtype == "object" else df["value"], errors='coerce')

    exclude_items = [
        "World",
        "Europe",
        "Eastern Europe",
        "Western Europe",
        "Northern Europe",
        "Southern Europe",
        "Asia",
        "Eastern Asia",
        "Eastern Asia and South-eastern Asia",
        "Southern Asia",
        "Southern Asia (excluding India)",
        "South-eastern Asia",
        "Central Asia and Southern Asia",
        "Central Asia",
        "Western Asia",
        "Africa",
        "Eastern Africa",
        "Middle Africa",
        "Northern Africa",
        "Southern Africa",
        "Western Africa",
        "Western Asia and Northern Africa",
        "Sub-Saharan Africa (including Sudan)",
        "Sub-Saharan Africa",
        "Northern Africa (excluding Sudan)",
        "Latin America and the Caribbean",
        "Northern America",
        "Central America",
        "South America",
        "Northern America and Europe",
        "Oceania",
        "Oceania excluding Australia and New Zealand",
        "European Union (27)",
        "High-income economies",
        "Low-income economies",
        "Lower-middle-income economies",
        "Upper-middle-income economies",
        "Least Developed Countries (LDCs)",
        "Small Island Developing States (SIDS)",
        "Land Locked Developing Countries (LLDCs)",
        "Low Income Food Deficit Countries (LIFDCs)"
    ]
    df = df[~(df['area'].isin(exclude_items))]

    # Garder les colonnes utiles
    df_pop = df_pop[['country.value','date','value']]
    df_pop = df_pop.rename(columns={
        'country.value':'area',
        'date':'year',
        'value':'value'
    })

    # Convertir l’année en int, la valeur en float
    df_pop['year'] = df_pop['year'].astype(int)
    df_pop['value'] = pd.to_numeric(df_pop['value'], errors='coerce')

    # Sauvegarde des données nettoyées dans une base sqlite3
    df.to_sql('clean_data', conn, if_exists='replace', index=False)
    df_pop.to_sql('clean_pop_tot', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Données nettoyées sauvegardées dans la base de données : {bdd_path}")

if __name__ == "__main__":
    clean_data()