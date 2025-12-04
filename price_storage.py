"""
Sistema di storage per salvare e gestire lo storico dei prezzi dei voli
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class PriceStorage:
    """Gestisce il salvataggio e recupero dello storico prezzi"""
    
    def __init__(self, db_file='price_history.json'):
        """
        Inizializza lo storage
        
        Args:
            db_file (str): Path del file JSON per salvare i dati
        """
        self.db_file = db_file
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Crea il file DB se non esiste"""
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump({'searches': []}, f, indent=2)
    
    def save_search(self, origin: str, destination: str, departure_date: str,
                    return_date: Optional[str], offers: List[Dict]):
        """
        Salva una ricerca e i suoi risultati
        
        Args:
            origin: Codice IATA aeroporto partenza
            destination: Codice IATA aeroporto destinazione
            departure_date: Data partenza
            return_date: Data ritorno (None per solo andata)
            offers: Lista delle offerte trovate
        """
        data = self._load_data()
        
        search_record = {
            'timestamp': datetime.now().isoformat(),
            'route': {
                'origin': origin,
                'destination': destination,
                'departure_date': departure_date,
                'return_date': return_date
            },
            'offers_count': len(offers),
            'cheapest_price': min([o['price']['total'] for o in offers]) if offers else None,
            'average_price': sum([o['price']['total'] for o in offers]) / len(offers) if offers else None,
            'currency': offers[0]['price']['currency'] if offers else 'EUR',
            'offers': offers
        }
        
        data['searches'].append(search_record)
        self._save_data(data)
    
    def get_price_history(self, origin: str, destination: str, 
                         departure_date: str, return_date: Optional[str] = None) -> List[Dict]:
        """
        Recupera lo storico prezzi per una specifica rotta
        
        Returns:
            List[Dict]: Lista degli storici di ricerca per quella rotta
        """
        data = self._load_data()
        
        history = [
            search for search in data['searches']
            if (search['route']['origin'] == origin and
                search['route']['destination'] == destination and
                search['route']['departure_date'] == departure_date and
                search['route']['return_date'] == return_date)
        ]
        
        return history
    
    def get_price_trend(self, origin: str, destination: str,
                       departure_date: str, return_date: Optional[str] = None) -> Dict:
        """
        Analizza il trend dei prezzi per una rotta
        
        Returns:
            Dict: Statistiche sul trend dei prezzi
        """
        history = self.get_price_history(origin, destination, departure_date, return_date)
        
        if not history:
            return {
                'found': False,
                'message': 'Nessuno storico disponibile per questa rotta'
            }
        
        prices = [h['cheapest_price'] for h in history if h['cheapest_price']]
        
        if not prices:
            return {
                'found': False,
                'message': 'Nessun prezzo disponibile'
            }
        
        return {
            'found': True,
            'searches_count': len(history),
            'lowest_price': min(prices),
            'highest_price': max(prices),
            'average_price': sum(prices) / len(prices),
            'current_price': prices[-1],
            'price_change': prices[-1] - prices[0] if len(prices) > 1 else 0,
            'currency': history[0]['currency'],
            'first_search': history[0]['timestamp'],
            'last_search': history[-1]['timestamp']
        }
    
    def get_all_routes(self) -> List[Dict]:
        """
        Recupera tutte le rotte monitorate
        
        Returns:
            List[Dict]: Lista delle rotte uniche monitorate
        """
        data = self._load_data()
        routes = {}
        
        for search in data['searches']:
            route = search['route']
            key = f"{route['origin']}-{route['destination']}-{route['departure_date']}-{route.get('return_date')}"
            
            if key not in routes:
                routes[key] = {
                    'route': route,
                    'searches_count': 0,
                    'last_search': None,
                    'last_price': None
                }
            
            routes[key]['searches_count'] += 1
            routes[key]['last_search'] = search['timestamp']
            routes[key]['last_price'] = search['cheapest_price']
        
        return list(routes.values())
    
    def _load_data(self) -> Dict:
        """Carica i dati dal file JSON"""
        with open(self.db_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data: Dict):
        """Salva i dati nel file JSON"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
