from dash import html, dcc

def create_year_options(df):
    # Crée les options pour le dropdown des années (une option par année unique dans la base de données)
    return [{"label": str(year), "value": year} for year in sorted(df["year"].unique())]

def create_indicator_options():
    """ 
    Crée les options pour le dropdown des indicateurs :
    - Prévalence de la sous alimentation (%)
    - Population obèse (millions)
    - Disponibilité alimentaire par habitant (kcal/personne/jour)
    """
    return [
        {"label": "Prevalence of undernourishment", 
         "value": "Prevalence of undernourishment (percent) (3-year average)"},
        {"label": "Number of people undernourished", 
         "value": "Number of people undernourished (million) (3-year average)"},
        {"label": "Prevalence of obesity in the adult population", 
         "value": "Prevalence of obesity in the adult population (18 years and older) (percent)"},
        {"label": "Number of obese adults", 
         "value": "Number of obese adults (18 years and older) (million)"},
        {"label": "Dietary energy supply", 
         "value": "Dietary energy supply used in the estimation of the prevalence of undernourishment (kcal/cap/day)"}
    ]

def filter_component(df):
    # Crée le composant de filtres avec les dropdowns pour l'année et l'indicateur
    return html.Div([
        # Dropdown pour sélectionner l'année
        html.Label("Select a year", style={"color": "white", "marginBottom": "10px"}),
        dcc.Dropdown(
            id="year-dropdown",
            options=create_year_options(df),
            value=df["year"].min(),
            style={"marginBottom": "20px", "color": "black"}
        ),
        # Dropdown pour sélectionner l'indicateur
        html.Label("Select an indicator", style={"color": "white", "marginBottom": "10px"}),
        dcc.Dropdown(
            id="indicator-dropdown",
            options=create_indicator_options(),
            value="Number of obese adults (18 years and older) (million)",
            style={"color": "black"},
            multi=False
        )
    ],
    # Styles pour le composant filtre
    style={
        "width": "225.7px",
        "backgroundColor": "#000000",
        "padding": "15px",
        "borderRadius": "0 10px 10px 0",
        "border": "1px solid white",
        "borderLeft": "none",
        "height": "355.2px",
        "position": "absolute",
        "left": "0px",
        "top": "40px",
    })