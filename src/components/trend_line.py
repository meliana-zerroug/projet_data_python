from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def prepare_trend_data(df):
    """
    Prépare les données pour les 3 indicateurs
    """
    # Définir les 2 indicateurs
    indicators = [
        "Number of obese adults (18 years and older) (million)",
        "Number of people undernourished (million) (3-year average)"
    ]
    
    trend_data = {}
    
    for indicator in indicators:
        indicator_df = df[df['item'] == indicator].copy()
        if not indicator_df.empty:
            yearly_data = indicator_df.groupby('year')['value'].mean().reset_index()
            yearly_data = yearly_data.sort_values('year')
            trend_data[indicator] = yearly_data
    
    return trend_data

def create_trend_figure(trend_data):
    """
    Crée la figure avec les 2 courbes
    """
    # Noms simplifiés pour la légende
    display_names = {
        "Number of people undernourished (million) (3-year average)": "Number of people undernourished (millions)",
        "Number of obese adults (18 years and older) (million)": "Number of obese adults (millions)"
    }
    
    # Couleurs pour chaque courbe
    colors = ['#7efbdb', '#7ed957']
    
    fig = go.Figure()
    
    for i, (indicator, data) in enumerate(trend_data.items()):
        if not data.empty:
            fig.add_trace(go.Scatter(
                x=data['year'],
                y=data['value'],
                mode='lines+markers',
                line=dict(color=colors[i], width=2),
                marker=dict(size=6, color=colors[i]),
                name=display_names[indicator]
            ))
    
    # Mise en forme
    fig.update_layout(
        title="Change in Indicators in bad nutrition in the world",
        xaxis_title="year",
        yaxis_title="value",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        height=400,
        margin=dict(l=50, r=50, t=50, b=50),
        legend=dict(
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='white',
            borderwidth=1,
            font=dict(color='white'),
            orientation="h",  # Légende horizontale
            yanchor="top",    # Ancrage en haut de la légende
            y=-0.3,           # Position en dessous du graphique
            xanchor="center", # Centrée horizontalement
            x=0.5
        )
    )
    
    return fig

def trend_line_component(df):
    """
    Composant principal pour la courbe de tendance avec style intégré
    """
    # Préparer les données
    trend_data = prepare_trend_data(df)
    
    # Créer la figure
    fig = create_trend_figure(trend_data)
    
    return html.Div([
        dcc.Graph(figure=fig)
    ],
    style={
            "width": "491.5px",
            "backgroundColor": "#000000",
            "padding": "10px",
            "borderRadius": "10px",
            "border": "1px solid white",
            "position": "absolute",
            "left": "750px",
            "top": "485px",
            "height": "355.3px",
    })