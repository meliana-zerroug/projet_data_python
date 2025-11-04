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

def filter_component(df):
    # Crée le composant de filtres avec les dropdowns pour l'année et l'indicateur
    return html.Div([
        html.Label("Select a year", style={"color": "white", "marginBottom": "10px"}),
        dcc.Dropdown(
            id="year-dropdown",
            options=create_year_options(df),
            value=df["année"].min(),
            style={"marginBottom": "20px", "color": "black"}
        ),
        html.Label("Select an indicator", style={"color": "white", "marginBottom": "10px"}),
        dcc.Dropdown(
            id="indicator-dropdown",
            options=create_indicator_options(),
            value="Nombre d'adultes (18 ans ou plus) obèses (millions)",
            style={"color": "black"},
            multi=False
        )
    ],
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