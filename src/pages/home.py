from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
from src.components.filter_component import filter_component
from src.components.map_component import map_component
from src.components.trend_line import trend_line_component
from src.utils.country_mapping import country_mapping


# Initialisation de l'application Dash 
app = Dash(__name__)

# Load data
#df = pd.read_csv("data/cleaned/clean_data.csv")
bdd_path = "data/raw/faostat_data.db"
con = sqlite3.connect(bdd_path)
df = pd.read_sql_query("SELECT * FROM raw_data", con)
con.close()

# Créer un masque pour filtrer les données pertinentes
mask_nutrition = df["Value"].notna()

# Appliquer le filtre et normaliser les noms des pays
df = df[mask_nutrition].copy()
df["Area"] = df["Area"].replace(country_mapping)

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
                trend_line_component(df)
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
    filtered_df = df[df["Year"] == selected_year].copy()
    
    # Filtrer par indicateur sélectionné
    indicator_mask = filtered_df["Item"] == selected_indicator
    country_data = filtered_df[indicator_mask].groupby("Area")["Value"].mean().reset_index()
        
    # Créer la carte en utilisant la fonction du composant map
    from src.components.map_component import create_choropleth
    fig = create_choropleth(country_data, selected_indicator, selected_year)

    return fig

if __name__ == "__main__":
    app.run(debug=True)
