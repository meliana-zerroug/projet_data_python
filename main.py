from dash import html
from src.pages.home import app

# Titre de la page
app.title = "Dashboard"

# Lancer le serveur
if __name__ == "__main__":
    app.run(debug=False)
