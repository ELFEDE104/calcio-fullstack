from flask import Flask
from flask_cors import CORS
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG
from routes_visualizzazione import visualizzazione_bp
from routes_gestione import gestione_bp

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

app.register_blueprint(visualizzazione_bp)
app.register_blueprint(gestione_bp)

@app.route('/')
def index():
    return {'messaggio': 'API Calcio funzionante ✅'}, 200

if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)