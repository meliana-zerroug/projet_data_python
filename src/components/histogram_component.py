from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def prepare_histo_data(df, selected_year, bins=20, gdp_bins=None):
    """
    Prépare un DataFrame agrégé par classe de PIB (gdp per capita) pour l'année donnée.
    Retour attendu : colonnes ['gdp_bin','gdp_per_capita_mean','obese_million','undernourished_million']
    - bins : nombre de classes de PIB (quantiles si possible)
    - gdp_bins : liste d'intervalles (edges) personnalisés, ex. [0,1000,5000,20000,1e6]
    """
    obese_item = "Number of obese adults (18 years and older) (million)"
    under_item = "Number of people undernourished (million) (3-year average)"
    gdp_item = "Gross domestic product per capita, PPP, (constant 2021 international $)"

    # détecter colonne zone/pays
    if 'area' not in df.columns or 'item' not in df.columns or 'value' not in df.columns or 'year' not in df.columns:
        return pd.DataFrame(columns=['gdp_bin','gdp_per_capita_mean','obese_million','undernourished_million'])

    subset = df.copy()
    subset['year'] = subset['year'].astype(int)
    subset = subset[subset['year'] == int(selected_year)]

    if subset.empty:
        return pd.DataFrame(columns=['gdp_bin','gdp_per_capita_mean','obese_million','undernourished_million'])

    # pivot pour avoir une colonne par item au niveau pays
    pivot = subset.pivot_table(index='area', columns='item', values='value', aggfunc='mean').reset_index()

    def safe_col(piv, col_name):
        if col_name in piv.columns:
            return pd.to_numeric(piv[col_name], errors='coerce')
        return pd.Series(np.nan, index=piv.index)

    pivot['obese_million'] = safe_col(pivot, obese_item).fillna(0.0)
    pivot['undernourished_million'] = safe_col(pivot, under_item).fillna(0.0)
    pivot['gdp_per_capita'] = safe_col(pivot, gdp_item)

    # enlever lignes sans GDP connu
    pivot = pivot.dropna(subset=['gdp_per_capita']).copy()
    if pivot.empty:
        return pd.DataFrame(columns=['gdp_bin','gdp_per_capita_mean','obese_million','undernourished_million'])

    # construire classes de GDP :
    # - si gdp_bins fourni (liste d'edges) on utilise pd.cut avec ces edges
    # - sinon on tente pd.qcut(bins) puis fallback sur pd.cut(bins)
    if gdp_bins is not None:
        # gdp_bins doit être une séquence d'edges (ex: [0,1000,5000,20000,1e6])
        pivot['gdp_bin'] = pd.cut(pivot['gdp_per_capita'], bins=gdp_bins, include_lowest=True)
    else:
        try:
            pivot['gdp_bin'] = pd.qcut(pivot['gdp_per_capita'], q=bins, duplicates='drop')
        except Exception:
            pivot['gdp_bin'] = pd.cut(pivot['gdp_per_capita'], bins=bins)

    # agréger par bin : somme des personnes (millions) et moyenne du PIB
    agg = pivot.groupby('gdp_bin').agg(
        obese_million=('obese_million', 'sum'),
        undernourished_million=('undernourished_million', 'sum'),
        gdp_per_capita_mean=('gdp_per_capita', 'mean'),
        countries_count=('area', 'nunique')
    ).reset_index()

    # pour lisibilité, ajouter un label numérique pour l'abscisse (moyenne de la classe)
    agg = agg.sort_values('gdp_per_capita_mean').reset_index(drop=True)
    # si gdp_bins fourni -> utiliser la représentation de l'intervalle, sinon la moyenne
    if gdp_bins is not None:
        agg['gdp_label'] = agg['gdp_bin'].astype(str).str.replace('Interval\\(', '').str.replace('\\)', '')
    else:
        agg['gdp_label'] = agg['gdp_per_capita_mean'].round(0).astype(int).apply(lambda v: f"{v:,d}".replace(',', ' '))
    # colonnes finales
    histo_df = agg[['gdp_label', 'gdp_per_capita_mean', 'obese_million', 'undernourished_million']].rename(
        columns={'gdp_label': 'gdp_bin'}
    )

    return histo_df

def create_histo_figure(histo_df, selected_year, gdp_bins=[0,1000,5000,10000,20000,50000,1e7]):
    """
    Crée un histogramme où l'abscisse est la classe de PIB (gdp_bin -> label),
    les barres montrent le total de personnes sous-alimentées / obèses (millions) par classe,
    et on affiche en ligne la moyenne du PIB par classe pour repère.
    Attendu : colonnes ['gdp_bin','gdp_per_capita_mean','obese_million','undernourished_million']
    """
    if histo_df is None or histo_df.empty:
        fig = go.Figure()
        fig.update_layout(title="Aucune donnée disponible pour l'histogramme 2020")
        return fig

    df = histo_df.copy()
    x = [str(gdp_bins[i]) + " - " + str(gdp_bins[i+1]) for i in range(len(gdp_bins) - 2)]                 # labels lisibles (ex: "1 234")
    obese_y = df['obese_million'].tolist()
    under_y = df['undernourished_million'].tolist()
    gdp_y = df['gdp_per_capita_mean'].tolist()

    fig = go.Figure()
    # barres empilées ou groupées selon préférence ; ici stacked pour montrer total par classe
    fig.add_trace(go.Bar(
        x=x,
        y=under_y,
        name='Undernourished (millions)',
        marker_color='#7efbdb',
        hovertemplate='GDP: %{x} $/hab<br>Undernourished: %{y:.2f} M'
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=obese_y,
        name='Obese adults (millions)',
        marker_color='#7ed957',
        hovertemplate='GDP: %{x} $/hab<br>Obese: %{y:.2f} M'
    ))

    fig.update_layout(
        title="Population undernourished and obese by GDP (" + str(selected_year) + ")",
        xaxis_title="GDP by person",
        yaxis=dict(title="Population (millions)"),
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=500,
        margin=dict(l=60, r=80, t=80, b=150),
        legend=dict(
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='white',
            borderwidth=1,
            font=dict(color='white'),
            orientation="h",  # Légende horizontale
            yanchor="top",    # Ancrage en haut de la légende
            y=-1,           # Position en dessous du graphique
            xanchor="center", # Centrée horizontalement
            x=0.5
        ),
    )

    fig.update_xaxes(tickangle=45, type='category')

    return fig

def histo_component(df):
    """
    Composant principal pour l'histogramme - retourne juste le conteneur avec un graphique vide
    Le contenu sera mis à jour par callback
    """
    return html.Div([
        dcc.Graph(id="histogram-graph", figure={})
    ],
    style={
            "width": "620px",
            "backgroundColor": "#000000",
            "padding": "10px",
            "borderRadius": "10px",
            "border": "1px solid white",
            "position": "absolute",
            "left": "0px",
            "top": "485px",
            "height": "355.3px",
    })