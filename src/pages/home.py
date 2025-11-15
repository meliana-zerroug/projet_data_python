from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from src.components.filter_component import filter_component
from src.components.map_component import map_component
from src.components.trend_line import trend_line_component
from src.components.histogram_component import histo_component, prepare_histo_data, create_histo_figure
from src.components.top_3 import top_countries_component, update_top_countries
from src.components.filled_area import filled_area_component, create_filled_area_figure
from src.utils.clean_data import clean_data

# Initialisation de l'application Dash 
app = Dash(__name__)

# Load data
bdd_path = "faostat_data.db"
con = sqlite3.connect(bdd_path)

cur = con.cursor()
cur.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)
trouvees = {row[0] for row in cur.fetchall()}
if 'clean_data' not in trouvees or 'clean_pop_tot' not in trouvees:
    clean_data()

df = pd.read_sql_query("SELECT * FROM clean_data", con)
df_pop = pd.read_sql_query("SELECT * FROM clean_pop_tot", con)
con.close()

# Créer un masque pour filtrer les données pertinentes
mask_nutrition = df["value"].notna()

# Appliquer le filtre et normaliser les noms des pays
df = df[mask_nutrition].copy()

# Layout principal
app.layout = html.Div(
    style={
        "backgroundColor": "#000000", 
        "color": "white", 
        "minHeight": "100vh", 
        "padding": "20px", 
        "fontFamily": "Arial"
    },
    children=[
        html.H1("Dashboard on Food Security Indicators", style={"textAlign": "center", "color": "white", "marginBottom": "20px"}),
        html.Div(
            style={
                "position": "relative",
                "width": "100%",
                "height": "100vh",
                "padding": "0",
                "overflow": "auto" 
            },
            children=[
                filter_component(df),
                map_component(),
                trend_line_component(df),
                top_countries_component(df),
                histo_component(df),
                filled_area_component(df)
            ]
        )
    ]
)

# Callback pour mettre à jour la carte en fonction du filtre 
@app.callback(
    Output("map-graph", "figure"),
    [Input("indicator-dropdown", "value"),
     Input("year-dropdown", "value")]
)
def update_map(selected_indicator, selected_year):
    if not selected_indicator or not selected_year:
        return {}
    
    # Filtrer par année
    filtered_df = df[df["year"] == selected_year].copy()
    
    # Filtrer par indicateur sélectionné
    indicator_mask = filtered_df["item"] == selected_indicator
    country_data = filtered_df[indicator_mask].groupby("area")["value"].mean().reset_index()
        
    # Créer la carte en utilisant la fonction du composant map
    from src.components.map_component import create_choropleth
    fig = create_choropleth(country_data, selected_indicator, selected_year)

    return fig

# Callback pour mettre à jour le top 3 des pays
@app.callback(
    Output("top-countries-list", "children"),
    [Input("indicator-dropdown", "value"),
     Input("year-dropdown", "value")]
)

def update_top_countries_list(selected_indicator, selected_year):
    return update_top_countries(df, selected_indicator, selected_year)

#Callback pour mettre à jour l'histogramme en fonction de l'année 
@app.callback(
    Output("histogram-graph", "figure"),
    [Input("year-dropdown", "value")]
)
def update_histogram(selected_year):
    if not selected_year:
        return {}
    
    # Définir les classes de PIB pour l'histogramme
    gdp_bins = [0, 2500, 5000, 7500, 10000, 15000, 20000, 50000, 75000, 1e6]
    
    # Préparer les données et créer la figure
    histo_data = prepare_histo_data(df, selected_year, gdp_bins=gdp_bins)
    fig = create_histo_figure(histo_data, selected_year, gdp_bins)
    
    return fig

# Callback pour mettre à jour le filled area plot en fonction de l'année
@app.callback(
    Output("filled-area-graph", "figure"),
    [Input("year-dropdown", "value")]
)
def update_filled_area(selected_year):
    if not selected_year:
        return {}
    
    # Définir les mêmes intervalles de PIB que l'histogramme
    gdp_bins = [0, 2500, 5000, 7500, 10000, 15000, 20000, 50000, 75000, 1e6]
    fig = create_filled_area_figure(df, df_pop, selected_year, gdp_bins)
    return fig

if __name__ == "__main__":
    app.run(debug=False)
