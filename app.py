"""
Flight Price Tracker - Web App con Flask
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from amadeus_client import AmadeusFlightClient
from price_storage import PriceStorage
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Inizializza client e storage
try:
    client = AmadeusFlightClient()
    storage = PriceStorage()
    api_ready = True
except ValueError as e:
    print(f"⚠️ API non configurata: {e}")
    client = None
    storage = PriceStorage()
    api_ready = False


@app.route('/')
def index():
    """Pagina principale"""
    return render_template('index.html', api_ready=api_ready)


@app.route('/api/search', methods=['POST'])
def search_flights():
    """Endpoint per cercare voli"""
    if not api_ready:
        return jsonify({
            'success': False,
            'error': 'API non configurata. Controlla il file .env'
        }), 500
    
    data = request.json
    origin = data.get('origin', '').strip().upper()
    destination = data.get('destination', '').strip().upper()
    departure_date = data.get('departure_date', '').strip()
    return_date = data.get('return_date', '').strip() or None
    adults = int(data.get('adults', 1))
    
    # Validazione
    if not origin or not destination or not departure_date:
        return jsonify({
            'success': False,
            'error': 'Compila tutti i campi obbligatori'
        }), 400
    
    try:
        # Ricerca voli
        if return_date:
            offers = client.search_round_trip(
                origin, destination, departure_date, return_date, adults
            )
        else:
            offers = client.search_flights(
                origin, destination, departure_date, adults
            )
        
        # Salva risultati
        if offers:
            storage.save_search(origin, destination, departure_date, return_date, offers)
        
        return jsonify({
            'success': True,
            'offers': offers,
            'count': len(offers)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_price_history():
    """Endpoint per ottenere lo storico prezzi"""
    origin = request.args.get('origin', '').strip().upper()
    destination = request.args.get('destination', '').strip().upper()
    departure_date = request.args.get('departure_date', '').strip()
    return_date = request.args.get('return_date', '').strip() or None
    
    if not origin or not destination or not departure_date:
        return jsonify({
            'success': False,
            'error': 'Parametri mancanti'
        }), 400
    
    trend = storage.get_price_trend(origin, destination, departure_date, return_date)
    
    return jsonify({
        'success': True,
        'trend': trend
    })


@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Endpoint per ottenere tutte le rotte monitorate"""
    routes = storage.get_all_routes()
    
    return jsonify({
        'success': True,
        'routes': routes,
        'count': len(routes)
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """Endpoint per verificare lo stato dell'API"""
    return jsonify({
        'success': True,
        'api_ready': api_ready
    })


if __name__ == '__main__':
    print("\n" + "="*50)
    print("✈️  FLIGHT PRICE TRACKER - WEB APP")
    print("="*50)
    if api_ready:
        print("✅ API Amadeus configurata correttamente")
    else:
        print("⚠️  API Amadeus non configurata")
        print("   Configura le credenziali nel file .env")
    print("\n🌐 Server in esecuzione su: http://localhost:5000")
    print("   Premi CTRL+C per terminare\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
