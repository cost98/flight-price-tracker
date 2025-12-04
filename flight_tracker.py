"""
Flight Price Tracker - Script principale
Traccia i prezzi dei voli e monitora le variazioni nel tempo
"""
import sys
from datetime import datetime
from amadeus_client import AmadeusFlightClient
from price_storage import PriceStorage


def format_price(price_info):
    """Formatta il prezzo per la visualizzazione"""
    return f"{price_info['total']:.2f} {price_info['currency']}"


def format_datetime(dt_string):
    """Formatta data/ora per visualizzazione"""
    dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
    return dt.strftime('%d/%m/%Y %H:%M')


def print_flight_details(flight):
    """Stampa i dettagli di un volo"""
    print(f"\n💰 Prezzo: {format_price(flight['price'])}")
    
    for idx, itinerary in enumerate(flight['itineraries'], 1):
        if len(flight['itineraries']) > 1:
            print(f"\n{'Andata' if idx == 1 else 'Ritorno'}:")
        
        print(f"  Durata totale: {itinerary['duration']}")
        
        for seg_idx, segment in enumerate(itinerary['segments'], 1):
            print(f"\n  Segmento {seg_idx}:")
            print(f"    {segment['departure']['iataCode']} → {segment['arrival']['iataCode']}")
            print(f"    Partenza: {format_datetime(segment['departure']['at'])}")
            print(f"    Arrivo: {format_datetime(segment['arrival']['at'])}")
            print(f"    Volo: {segment['carrier']}{segment['flight_number']}")
            print(f"    Durata: {segment['duration']}")


def search_flights(client, storage):
    """Interfaccia per cercare voli"""
    print("\n🔍 RICERCA VOLI")
    print("=" * 50)
    
    origin = input("Aeroporto di partenza (es: FCO per Roma): ").strip().upper()
    destination = input("Aeroporto di destinazione (es: JFK per New York): ").strip().upper()
    departure_date = input("Data partenza (YYYY-MM-DD): ").strip()
    
    trip_type = input("Andata e ritorno? (s/n): ").strip().lower()
    return_date = None
    if trip_type == 's':
        return_date = input("Data ritorno (YYYY-MM-DD): ").strip()
    
    adults = input("Numero passeggeri adulti (default 1): ").strip()
    adults = int(adults) if adults else 1
    
    print("\n⏳ Ricerca in corso...")
    
    if return_date:
        offers = client.search_round_trip(
            origin, destination, departure_date, return_date, adults
        )
    else:
        offers = client.search_flights(
            origin, destination, departure_date, adults
        )
    
    if not offers:
        print("❌ Nessun volo trovato.")
        return
    
    # Salva i risultati
    storage.save_search(origin, destination, departure_date, return_date, offers)
    
    print(f"\n✅ Trovati {len(offers)} voli!")
    print(f"💾 Risultati salvati nello storico")
    
    # Mostra il più economico
    cheapest = min(offers, key=lambda x: x['price']['total'])
    print(f"\n🏆 VOLO PIÙ ECONOMICO:")
    print_flight_details(cheapest)
    
    # Mostra altri risultati
    show_all = input("\n\nMostrare tutti i risultati? (s/n): ").strip().lower()
    if show_all == 's':
        for idx, offer in enumerate(offers[1:], 2):
            print(f"\n{'='*50}")
            print(f"Opzione {idx}:")
            print_flight_details(offer)


def view_price_history(storage):
    """Visualizza lo storico prezzi"""
    print("\n📊 STORICO PREZZI")
    print("=" * 50)
    
    origin = input("Aeroporto di partenza: ").strip().upper()
    destination = input("Aeroporto di destinazione: ").strip().upper()
    departure_date = input("Data partenza (YYYY-MM-DD): ").strip()
    
    has_return = input("Con ritorno? (s/n): ").strip().lower()
    return_date = None
    if has_return == 's':
        return_date = input("Data ritorno (YYYY-MM-DD): ").strip()
    
    trend = storage.get_price_trend(origin, destination, departure_date, return_date)
    
    if not trend['found']:
        print(f"\n❌ {trend['message']}")
        return
    
    print(f"\n📈 TREND PREZZI per {origin} → {destination}")
    print(f"   Partenza: {departure_date}")
    if return_date:
        print(f"   Ritorno: {return_date}")
    
    print(f"\n   Ricerche effettuate: {trend['searches_count']}")
    print(f"   Prima ricerca: {format_datetime(trend['first_search'])}")
    print(f"   Ultima ricerca: {format_datetime(trend['last_search'])}")
    print(f"\n   💰 Prezzo più basso: {trend['lowest_price']:.2f} {trend['currency']}")
    print(f"   💰 Prezzo più alto: {trend['highest_price']:.2f} {trend['currency']}")
    print(f"   💰 Prezzo medio: {trend['average_price']:.2f} {trend['currency']}")
    print(f"   💰 Prezzo attuale: {trend['current_price']:.2f} {trend['currency']}")
    
    if trend['price_change'] != 0:
        emoji = "📉" if trend['price_change'] < 0 else "📈"
        print(f"\n   {emoji} Variazione: {trend['price_change']:+.2f} {trend['currency']}")


def view_all_routes(storage):
    """Visualizza tutte le rotte monitorate"""
    print("\n🗺️  ROTTE MONITORATE")
    print("=" * 50)
    
    routes = storage.get_all_routes()
    
    if not routes:
        print("❌ Nessuna rotta monitorata ancora.")
        return
    
    for idx, route_info in enumerate(routes, 1):
        route = route_info['route']
        print(f"\n{idx}. {route['origin']} → {route['destination']}")
        print(f"   Partenza: {route['departure_date']}")
        if route['return_date']:
            print(f"   Ritorno: {route['return_date']}")
        print(f"   Ricerche: {route_info['searches_count']}")
        print(f"   Ultimo prezzo: {route_info['last_price']:.2f} EUR")
        print(f"   Ultima ricerca: {format_datetime(route_info['last_search'])}")


def main_menu():
    """Menu principale dell'applicazione"""
    print("\n" + "="*50)
    print("✈️  FLIGHT PRICE TRACKER")
    print("="*50)
    print("\n1. 🔍 Cerca voli")
    print("2. 📊 Visualizza storico prezzi")
    print("3. 🗺️  Visualizza rotte monitorate")
    print("4. 🚪 Esci")
    
    choice = input("\nScelta: ").strip()
    return choice


def main():
    """Funzione principale"""
    try:
        # Inizializza client e storage
        client = AmadeusFlightClient()
        storage = PriceStorage()
        
        print("\n✅ Client Amadeus inizializzato correttamente!")
        
        while True:
            choice = main_menu()
            
            if choice == '1':
                search_flights(client, storage)
            elif choice == '2':
                view_price_history(storage)
            elif choice == '3':
                view_all_routes(storage)
            elif choice == '4':
                print("\n👋 Arrivederci!")
                break
            else:
                print("\n❌ Scelta non valida.")
            
            input("\nPremi INVIO per continuare...")
    
    except ValueError as e:
        print(f"\n❌ Errore di configurazione: {e}")
        print("\nAssicurati di:")
        print("1. Aver creato un file .env")
        print("2. Aver inserito AMADEUS_API_KEY e AMADEUS_API_SECRET")
        print("3. Registrati su: https://developers.amadeus.com/register")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Arrivederci!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Errore imprevisto: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
