import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import os

# App initialisieren
app = dash.Dash(__name__)
app.title = "Bunkerverordnungen"

# Design: Farben und Schrift
font_family = "Barlow Condensed, sans-serif"
color_palette = [
    "#10225A",  # Blau
    "#D1655B",  # Coralle
    "#376179",  # Dunkleres Blau
    "#005B96",  # Blau
    "#4B85A6",  # Aqua
    "#939498",  # Grau
]

# GitHub Pages Basis-URL – bitte ggf. anpassen
MAP_BASE_URL = "https://chrigw.github.io"

# Mapping für Radio-Auswahl
map_files = {
    "Bundesländer": "dashboard_bundeslaender.html",
    "Häfen": "deutschland_haefen_karte.html",
    "Wasserstraßen": "deutschland_wasserstrassen_karte.html"
}

# Logo-URL und Link
logo_url = "https://raw.githubusercontent.com/chrigw/maritime-karten/a0a4b7daa13f049bda865d92f0539c1756c063e8/D-DMZ-Logo-4C%20HOCH.jpg"
link_url = "https://www.deutsches-maritimes-zentrum.de"

# Logo-Komponente
logo_html = html.Div([
    html.A([
        html.Img(src=logo_url, style={'height': '80px'})
    ], href=link_url, target="_blank")
], style={
    'position': 'fixed',
    'top': '10px',
    'right': '10px',
    'background-color': 'white',
    'padding': '20px',
    'lineHeight': '1.6',
    'border-radius': '8px',
    'box-shadow': '0 0 6px rgba(0,0,0,0.2)',
    'zIndex': 9999
})

# Layout
app.layout = html.Div([
    html.Div(style={'height': '10px'}),  # Kleineren Abstand nach oben eingestellt

    html.H1("Bunkerverordnungen", style={"color": color_palette[0], "fontFamily": font_family}),

    html.P(
        "Diese interaktive Karte bietet einen Überblick über Bunkervorschriften in Deutschland. "
        "Wählen Sie eine Kategorie, um spezifische Regelungen für Bundesländer, Häfen oder Wasserstraßen anzuzeigen.",
        style={"fontFamily": font_family, "fontSize": "18px", "lineHeight": "1.6", "color": color_palette[2]}
    ),

    html.Div([
        dcc.RadioItems(
            id='map-selector',
            options=[{'label': label, 'value': label} for label in map_files.keys()],
            value='Bundesländer',
            labelStyle={'display': 'inline-block', 'margin-right': '20px', 'fontFamily': font_family,
                        'fontSize': '16px'},
            style={'padding': '10px', 'color': color_palette[0]}
        )
    ], style={'backgroundColor': '#f9f9f9', 'padding': '10px', 'borderRadius': '8px',
              'boxShadow': '0 2px 4px rgba(0,0,0,0.05)', 'marginBottom': '20px'}),

    html.Iframe(
        id='map-frame',
        src=f"{MAP_BASE_URL}/{map_files['Bundesländer']}",
        style={'width': '100%', 'height': '600px', 'border': '1px solid #ccc', 'borderRadius': '8px'}
    )
], style={'padding': '30px', 'fontFamily': font_family})

# Callback zur Aktualisierung der Iframe-Quelle
@app.callback(
    Output('map-frame', 'src'),
    Input('map-selector', 'value')
)
def update_map(selection):
    return f"{MAP_BASE_URL}/{map_files[selection]}"

# Server starten
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
