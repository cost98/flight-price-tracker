"""
Client per l'API Amadeus - Ricerca voli e prezzi
"""
import os
from amadeus import Client, ResponseError
from dotenv import load_dotenv

# Carica variabili d'ambiente
load_dotenv()


class AmadeusFlightClient:
    """Client per interagire con l'API Amadeus"""
    
    def __init__(self):
        """Inizializza il client Amadeus con le credenziali"""
        api_key = os.getenv('AMADEUS_API_KEY')
        api_secret = os.getenv('AMADEUS_API_SECRET')
        
        if not api_key or not api_secret:
            raise ValueError(
                "AMADEUS_API_KEY e AMADEUS_API_SECRET devono essere configurati nel file .env"
            )
        
        self.client = Client(
            client_id=api_key,
            client_secret=api_secret
        )
    
    def search_flights(self, origin, destination, departure_date, adults=1, 
                      max_results=10, currency='EUR'):
        """
        Cerca voli disponibili
        
        Args:
            origin (str): Codice aeroporto IATA di partenza (es: 'FCO' per Roma)
            destination (str): Codice aeroporto IATA di destinazione (es: 'JFK' per New York)
            departure_date (str): Data di partenza formato YYYY-MM-DD
            adults (int): Numero di adulti
            max_results (int): Numero massimo di risultati
            currency (str): Valuta per i prezzi (EUR, USD, etc.)
        
        Returns:
            list: Lista di offerte voli con prezzi
        """
        try:
            response = self.client.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                adults=adults,
                max=max_results,
                currencyCode=currency
            )
            
            return self._parse_flight_offers(response.data)
            
        except ResponseError as error:
            print(f"Errore API Amadeus: {error}")
            return []
    
    def search_round_trip(self, origin, destination, departure_date, return_date,
                         adults=1, max_results=10, currency='EUR'):
        """
        Cerca voli andata e ritorno
        
        Args:
            origin (str): Codice aeroporto IATA di partenza
            destination (str): Codice aeroporto IATA di destinazione
            departure_date (str): Data di partenza formato YYYY-MM-DD
            return_date (str): Data di ritorno formato YYYY-MM-DD
            adults (int): Numero di adulti
            max_results (int): Numero massimo di risultati
            currency (str): Valuta per i prezzi
        
        Returns:
            list: Lista di offerte voli con prezzi
        """
        try:
            response = self.client.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                returnDate=return_date,
                adults=adults,
                max=max_results,
                currencyCode=currency
            )
            
            return self._parse_flight_offers(response.data)
            
        except ResponseError as error:
            print(f"Errore API Amadeus: {error}")
            return []
    
    def _parse_flight_offers(self, offers_data):
        """
        Parsifica i dati delle offerte voli
        
        Args:
            offers_data: Dati raw dall'API Amadeus
        
        Returns:
            list: Lista di dizionari con info voli semplificate
        """
        parsed_offers = []
        
        for offer in offers_data:
            flight_info = {
                'id': offer.get('id'),
                'price': {
                    'total': float(offer['price']['total']),
                    'currency': offer['price']['currency']
                },
                'itineraries': []
            }
            
            for itinerary in offer.get('itineraries', []):
                itinerary_info = {
                    'duration': itinerary.get('duration'),
                    'segments': []
                }
                
                for segment in itinerary.get('segments', []):
                    segment_info = {
                        'departure': {
                            'iataCode': segment['departure']['iataCode'],
                            'at': segment['departure']['at']
                        },
                        'arrival': {
                            'iataCode': segment['arrival']['iataCode'],
                            'at': segment['arrival']['at']
                        },
                        'carrier': segment.get('carrierCode'),
                        'flight_number': segment.get('number'),
                        'duration': segment.get('duration')
                    }
                    itinerary_info['segments'].append(segment_info)
                
                flight_info['itineraries'].append(itinerary_info)
            
            parsed_offers.append(flight_info)
        
        return parsed_offers
    
    def get_cheapest_flight(self, origin, destination, departure_date, 
                           return_date=None, adults=1, currency='EUR'):
        """
        Trova il volo più economico
        
        Returns:
            dict: Info del volo più economico o None se non trovato
        """
        if return_date:
            offers = self.search_round_trip(
                origin, destination, departure_date, return_date, 
                adults, max_results=50, currency=currency
            )
        else:
            offers = self.search_flights(
                origin, destination, departure_date, 
                adults, max_results=50, currency=currency
            )
        
        if not offers:
            return None
        
        # Ordina per prezzo e restituisci il più economico
        cheapest = min(offers, key=lambda x: x['price']['total'])
        return cheapest
