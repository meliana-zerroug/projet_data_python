from dash import html, dcc
import plotly.express as px

def create_choropleth(country_data, selected_indicator, selected_year):
    """
    Crée une carte choroplèthe avec les données fournies
    """
    # Création de la carte
    fig = px.choropleth(
        country_data,
        locations="area",
        locationmode="country names",
        color="value",
        scope="world",
        color_continuous_scale=[[0, "#ffffff"], [1, "#7efbdb"]],
        title=f"{selected_indicator} en {selected_year}",
        hover_name="area",
        hover_data={"area": False, "value": ":.1f"},
        labels={"value": "Number of people (millions)" },
    )
    
    # Personnalisation de la colorbar et du titre
    fig.update_layout(
        title=dict(
            text="World Map of " + (selected_indicator) + " (" + str(selected_year) + ")", 
            y=0.97,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(color='white', size=16)
        ),
        coloraxis_colorbar=dict(
            len=0.8,
            thickness=20,
            xanchor="center",
            x=0.5,
            y=0.2,
            yanchor="top",
            title=dict(text="", font=dict(size=14)),
            tickfont=dict(size=12),
            tickformat=".1f",
            orientation="h",
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0
        ),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font_color="white",
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type="equirectangular",
            bgcolor="black",
            coastlinecolor="white",
            landcolor="#333333",
            showland=True,
        )
    )
    
    return fig

def map_component():
    """
    Retourne le composant graphique de la carte
    """
    return html.Div(
        dcc.Graph(
            id="map-graph",
            style={
                "height": "100%", 
                "width": "100%",
            },
            config={"displayModeBar": False}
        ),
        style={
            "width": "690px",
            "backgroundColor": "#000000",
            "padding": "15px",
            "borderRadius": "10px",
            "border": "1px solid white",
            "position": "absolute",
            "left": "560px",
            "top": "40px",
            "height": "400px",
        }
    )
