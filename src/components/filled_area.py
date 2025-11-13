from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import sqlite3

def filled_area_component(df):
    """
    Crée un conteneur pour le filled area plot
    
    Args:
        df: DataFrame contenant les données
    
    Returns:
        html.Div: Conteneur avec le graphique
    """
    return html.Div(
        style={
            "width": "1250px",
            "backgroundColor": "#000000",
            "padding": "10px",
            "borderRadius": "10px",
            "border": "1px solid white",
            "position": "absolute",
            "left": "0px",
            "top": "920px",
            "height": "400px"
        },
        children=[
            dcc.Graph(
                id="filled-area-graph",
                config={"displayModeBar": False},
                style={"height": "380px"}
            )
        ]
    )

def prepare_filled_area_data(df, df_pop, selected_year, gdp_bins=None):
    """
    Prépare les données pour le filled area plot avec regroupement par intervalles de PIB
    
    Args:
        df: DataFrame avec les données FAOSTAT
        df_pop: DataFrame avec les données de population
        selected_year: Année sélectionnée
        gdp_bins: Liste d'intervalles de PIB (ex: [0, 2500, 5000, 10000, 50000, 1e7])
    
    Returns:
        DataFrame avec les colonnes gdp_bin_mid, obese_million, undernourished_million
    """
    gdp_item = "Gross domestic product per capita, PPP, (constant 2021 international $)"
    obese_item = "Number of obese adults (18 years and older) (million)"
    under_item = "Number of people undernourished (million) (3-year average)"
    
    # Intervalles par défaut si non fournis
    if gdp_bins is None:
        gdp_bins = [0, 2500, 5000, 7500, 10000, 15000, 20000, 50000, 1e7]
    
    # Convertir selected_year en string pour correspondre au format de df
    selected_year_str = str(selected_year)
    
    # Filtrer pour l'année sélectionnée
    subset = df[df['year'] == selected_year_str].copy()
    
    if subset.empty:
        return pd.DataFrame(columns=['gdp_bin_mid', 'obese_million', 'undernourished_million'])
    
    # Créer un pivot pour avoir toutes les données
    pivot = subset.pivot_table(index='area', columns='item', values='value', aggfunc='mean').reset_index()
    
    # Extraire les données de PIB
    if gdp_item in pivot.columns:
        pivot['gdp_per_capita'] = pd.to_numeric(pivot[gdp_item], errors='coerce')
    else:
        pivot['gdp_per_capita'] = pd.Series(dtype=float)
    
    # Extraire les données d'obésité et de sous-nutrition
    if obese_item in pivot.columns:
        pivot['obese_million'] = pd.to_numeric(pivot[obese_item], errors='coerce').fillna(0.0)
    else:
        pivot['obese_million'] = 0.0
        
    if under_item in pivot.columns:
        pivot['undernourished_million'] = pd.to_numeric(pivot[under_item], errors='coerce').fillna(0.0)
    else:
        pivot['undernourished_million'] = 0.0
    
    # Garder seulement les colonnes nécessaires
    pivot = pivot[['area', 'gdp_per_capita', 'obese_million', 'undernourished_million']].copy()
    pivot = pivot.dropna(subset=['gdp_per_capita'])
    
    if pivot.empty:
        return pd.DataFrame(columns=['gdp_bin_mid', 'obese_million', 'undernourished_million'])
    
    # Créer des intervalles de PIB
    pivot['gdp_bin'] = pd.cut(pivot['gdp_per_capita'], bins=gdp_bins, include_lowest=True)
    
    # Calculer le point milieu de chaque intervalle pour l'affichage
    pivot['gdp_bin_mid'] = pivot['gdp_bin'].apply(lambda x: (x.left + x.right) / 2 if pd.notna(x) else None)
    
    # Agréger par intervalle de PIB (somme des personnes)
    aggregated = pivot.groupby('gdp_bin_mid').agg({
        'obese_million': 'sum',
        'undernourished_million': 'sum'
    }).reset_index()
    
    # Trier par PIB
    aggregated = aggregated.sort_values('gdp_bin_mid').reset_index(drop=True)
    
    return aggregated

def create_filled_area_figure(df, df_pop, selected_year, gdp_bins=None):
    """
    Crée la figure du filled area plot
    
    Args:
        df: DataFrame avec les données FAOSTAT
        df_pop: DataFrame avec les données de population
        selected_year: Année sélectionnée
        gdp_bins: Liste d'intervalles de PIB
    
    Returns:
        Figure Plotly
    """
    # Intervalles par défaut
    if gdp_bins is None:
        gdp_bins = [0, 2500, 5000, 7500, 10000, 15000, 20000, 50000, 1e7]
    
    # Préparer les données
    data = prepare_filled_area_data(df, df_pop, selected_year, gdp_bins)
    
    if data.empty:
        # Retourner une figure vide avec un message
        fig = go.Figure()
        fig.add_annotation(
            text="Aucune donnée disponible pour cette année",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color="white")
        )
        fig.update_layout(
            plot_bgcolor='#1a1a1a',
            paper_bgcolor='#1a1a1a',
            font=dict(color='white'),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    # Créer les labels pour l'axe X (identiques à l'histogramme)
    x_labels = [str(gdp_bins[i]) + " - " + str(gdp_bins[i+1]) for i in range(len(gdp_bins) - 1)]
    
    # Créer le filled area plot avec deux traces
    fig = go.Figure()
    
    # Trace pour les personnes obèses
    fig.add_trace(go.Scatter(
        x=x_labels[:len(data)],
        y=data['obese_million'],
        fill='tozeroy',
        mode='lines+markers',
        name='Obese adults (millions)',
        line=dict(color='#7ed957', width=3, shape='spline'),
        marker=dict(size=8, color='#7ed957'),
        fillcolor='rgba(126, 217, 87, 0.3)',
        hovertemplate='GDP: %{x} $/hab<br>' +
                      'Obese: %{y:,.2f} M<br>' +
                      '<extra></extra>'
    ))
    
    # Trace pour les personnes sous-alimentées
    fig.add_trace(go.Scatter(
        x=x_labels[:len(data)],
        y=data['undernourished_million'],
        fill='tozeroy',
        mode='lines+markers',
        name='Undernourished (millions)',
        line=dict(color='#7efbdb', width=3, shape='spline'),
        marker=dict(size=8, color='#7efbdb'),
        fillcolor='rgba(126, 251, 219, 0.3)',
        hovertemplate='GDP: %{x} $/hab<br>' +
                      'Undernourished: %{y:,.2f} M<br>' +
                      '<extra></extra>'
    ))
    
    # Mise en forme du graphique
    fig.update_layout(
        title=dict(
            text=f'Obesity and Undernourishment by GDP ({selected_year})',
            font=dict(size=16, color='white'),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='GDP by person',
        yaxis_title='Population (millions)',
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial", size=12, color='white'),
        margin=dict(l=80, r=40, t=60, b=60),
        height=380,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='white',
            borderwidth=1,
            font=dict(color='white')
        )
    )
    
    # Style des axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#333333',
        showline=True,
        linewidth=1,
        linecolor='#666666',
        tickangle=45,
        type='category',
        color='white'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#333333',
        showline=True,
        linewidth=1,
        linecolor='#666666',
        tickformat=',',
        color='white'
    )
    
    return fig
