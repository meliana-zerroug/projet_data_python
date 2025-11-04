from dash import html, dcc

def create_year_options(df):
    # Crée les options pour le dropdown des années
    return [{"label": str(year), "value": year} for year in sorted(df["année"].unique())]

def create_indicator_options():
    # Crée les options pour le dropdown des indicateurs
    return [
        {"label": "Prévalence de la sous alimentation", 
         "value": "Prévalence de la sous-alimentation (%) (moyenne sur 3 ans)"},
        {"label": "Population obèse", 
         "value": "Nombre d'adultes (18 ans ou plus) obèses (millions)"},
        {"label": "Disponibilité alimentaire", 
         "value": "Disponibilité alimentaire par habitant utilisée dans l'estimation de la prévalence de la sous-alimentation (kcal/personne/jour)"}
    ]

