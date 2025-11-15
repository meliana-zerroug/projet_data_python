from dash import html, dcc
import pandas as pd

def top_countries_component(df):
    """
    Composant pour afficher le top 3 des pays avec la valeur la plus haute
    """
    return html.Div([
        #html.H3("Top 3 des Pays", style={'color': 'white', 'textAlign': 'center', 'marginBottom': '20px'}),
        html.Div(id='top-countries-list', style={'color': 'white', 'marginTop': '40px'})
    ],
    style={
        "width": "250px",
        "backgroundColor": "#000000",
        "padding": "15px",
        "borderRadius": "10px",
        "border": "1px solid white",
        "position": "absolute",
        "left": "270px",
        "top": "40px",
        "height": "400px",
    })

def update_top_countries(df, selected_indicator, selected_year):
    """
    Met à jour la liste du top 3 des pays en fonction des filtres
    """
    if not selected_indicator or not selected_year:
        return "Sélectionnez un indicateur et une année"
    
    # Filtrer les données
    filtered_df = df[
        (df['item'] == selected_indicator) & 
        (df['year'] == selected_year)
    ].copy()
    
    if filtered_df.empty:
        return "Aucune donnée disponible"
    
    # Trier par valeur décroissante et prendre le top 3
    top_countries = filtered_df.nlargest(3, 'value')[['area', 'value']]
    
    # Créer la liste formatée
    countries_list = []
    for i, (_, row) in enumerate(top_countries.iterrows(), 1):
        country_name = row['area']
        value = row['value']
        
        # Formater selon l'indicateur
        if "Prevalence" in selected_indicator:
            value_text = f"{value:.1f} %"
        elif "Number" in selected_indicator:
            value_text = f"{value:.1f} M"
        else:
            value_text = f"{value:.1f}"
        
        countries_list.append(
            html.Div([
                # CHIFFRE EN GROS AU-DESSUS
                html.Div(
                    value_text, 
                    style={
                        'color': '#7efbdb', 
                        'fontSize': '40px',  # Taille augmentée
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                        'marginBottom': '5px'
                    }
                ),
                # NOM DU PAYS EN DESSOUS
                html.Div(
                    f"#{i} {country_name}", 
                    style={
                        'color': 'white', 
                        'fontSize': '20px',
                        'textAlign': 'center',
                        'marginBottom': '15px'
                    }
                )
            ], style={'marginBottom': '10px'})
        )
    
    return html.Div(countries_list)