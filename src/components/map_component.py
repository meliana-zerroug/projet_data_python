from dash import html, dcc
import plotly.express as px

def create_choropleth(country_data, selected_indicator, selected_year):
    """
    Crée une carte choroplèthe avec les données fournies
    """
    # Création de la carte
    fig = px.choropleth(
        country_data,
        locations="zone",
        locationmode="country names",
        color="valeur",
        scope="world",
        color_continuous_scale=[[0, "#ffffff"], [1, "#7efbdb"]],
        title=f"{selected_indicator} en {selected_year}",
        hover_name="zone",
        hover_data={"zone": False, "valeur": ":.1f"},
        labels={"valeur": "Valeur"}
    )
    
