from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from src.components.filter_component import filter_component
from src.components.map_component import map_component

# Initialisation de l'application Dash 
app = Dash(__name__)

# Load data
df = pd.read_csv("data/cleaned/clean_data.csv")

# Liste des indicateurs pertinents pour la malnutrition et l'obésité
indicateurs_pertinents = [
    "Prévalence de la sous-alimentation (%) (moyenne sur 3 ans)",
    "Nombre d'adultes (18 ans ou plus) obèses (millions)",
    "Nombre de personnes sous-alimentées (millions) (moyenne sur 3 ans)",
    "Prévalence de l obésité chez l adulte  18 ans ou plus",
    "Disponibilité alimentaire par habitant utilisée dans l'estimation de la prévalence de la sous-alimentation (kcal/personne/jour)"
]

from src.utils.country_mapping import country_mapping

# Créer un masque pour filtrer les données pertinentes
mask_nutrition = df["valeur"].notna()

# Appliquer le filtre et normaliser les noms des pays
df = df[mask_nutrition].copy()
df["zone"] = df["zone"].replace(country_mapping)

# Préparation des données pour l'affichage
sample_data = df.groupby("zone")["valeur"].mean().head()