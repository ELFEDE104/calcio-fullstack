"""
app.py
------
Punto di avvio del server Flask.
Registra tutti i blueprint delle rotte.
"""

from flask import Flask
from flask_cors import CORS
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
from routes_visualizzazione import visualizzazione_bp

app = Flask(__name__)
CORS(app)

# Registra i blueprint
app.register_blueprint(visualizzazione_bp)

# Rotta di test
@app.route('/')
def index():
    return {'messaggio': 'API Calcio funzionante ✅'}, 200

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)