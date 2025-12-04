"""
Flight Price Tracker - GUI con Tkinter
Interfaccia grafica per tracciare prezzi voli
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import threading
from amadeus_client import AmadeusFlightClient
from price_storage import PriceStorage


class FlightTrackerGUI:
    """Interfaccia grafica per il Flight Price Tracker"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("✈️ Flight Price Tracker")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Inizializza client e storage
        try:
            self.client = AmadeusFlightClient()
            self.storage = PriceStorage()
            self.api_ready = True
        except ValueError as e:
            self.api_ready = False
            messagebox.showerror("Errore Configurazione", 
                               f"Errore API: {e}\n\nConfigura le credenziali nel file .env")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Crea tutti i widget dell'interfaccia"""
        # Titolo
        title_frame = tk.Frame(self.root, bg='#2196F3', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="✈️ Flight Price Tracker",
            font=('Arial', 20, 'bold'),
            bg='#2196F3',
            fg='white'
        )
        title_label.pack(pady=15)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Ricerca Voli
        self.search_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.search_tab, text='🔍 Ricerca Voli')
        self.create_search_tab()
        
        # Tab 2: Storico Prezzi
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text='📊 Storico Prezzi')
        self.create_history_tab()
        
        # Tab 3: Rotte Monitorate
        self.routes_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.routes_tab, text='🗺️ Rotte Monitorate')
        self.create_routes_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("✅ Pronto" if self.api_ready else "❌ API non configurata")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor='w',
            bg='#e0e0e0'
        )
        status_bar.pack(side='bottom', fill='x')
    
    def create_search_tab(self):
        """Crea il tab di ricerca voli"""
        # Frame principale
        main_frame = ttk.Frame(self.search_tab, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Form di ricerca
        form_frame = ttk.LabelFrame(main_frame, text="Parametri di Ricerca", padding="15")
        form_frame.pack(fill='x', pady=(0, 10))
        
        # Origine
        ttk.Label(form_frame, text="Aeroporto Partenza (IATA):").grid(row=0, column=0, sticky='w', pady=5)
        self.origin_var = tk.StringVar()
        origin_entry = ttk.Entry(form_frame, textvariable=self.origin_var, width=10)
        origin_entry.grid(row=0, column=1, sticky='w', pady=5, padx=5)
        ttk.Label(form_frame, text="es: FCO", foreground='gray').grid(row=0, column=2, sticky='w')
        
        # Destinazione
        ttk.Label(form_frame, text="Aeroporto Destinazione (IATA):").grid(row=1, column=0, sticky='w', pady=5)
        self.destination_var = tk.StringVar()
        destination_entry = ttk.Entry(form_frame, textvariable=self.destination_var, width=10)
        destination_entry.grid(row=1, column=1, sticky='w', pady=5, padx=5)
        ttk.Label(form_frame, text="es: JFK", foreground='gray').grid(row=1, column=2, sticky='w')
        
        # Data partenza
        ttk.Label(form_frame, text="Data Partenza:").grid(row=2, column=0, sticky='w', pady=5)
        self.departure_var = tk.StringVar()
        default_departure = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.departure_var.set(default_departure)
        ttk.Entry(form_frame, textvariable=self.departure_var, width=15).grid(row=2, column=1, sticky='w', pady=5, padx=5)
        ttk.Label(form_frame, text="YYYY-MM-DD", foreground='gray').grid(row=2, column=2, sticky='w')
        
        # Andata e ritorno
        self.roundtrip_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, text="Andata e Ritorno", variable=self.roundtrip_var,
                       command=self.toggle_return_date).grid(row=3, column=0, columnspan=2, sticky='w', pady=5)
        
        # Data ritorno
        ttk.Label(form_frame, text="Data Ritorno:").grid(row=4, column=0, sticky='w', pady=5)
        self.return_var = tk.StringVar()
        default_return = (datetime.now() + timedelta(days=37)).strftime('%Y-%m-%d')
        self.return_var.set(default_return)
        self.return_entry = ttk.Entry(form_frame, textvariable=self.return_var, width=15)
        self.return_entry.grid(row=4, column=1, sticky='w', pady=5, padx=5)
        ttk.Label(form_frame, text="YYYY-MM-DD", foreground='gray').grid(row=4, column=2, sticky='w')
        
        # Passeggeri
        ttk.Label(form_frame, text="Numero Passeggeri:").grid(row=5, column=0, sticky='w', pady=5)
        self.adults_var = tk.StringVar(value="1")
        ttk.Spinbox(form_frame, from_=1, to=9, textvariable=self.adults_var, width=5).grid(row=5, column=1, sticky='w', pady=5, padx=5)
        
        # Bottone ricerca
        search_btn = ttk.Button(
            form_frame,
            text="🔍 Cerca Voli",
            command=self.search_flights,
            style='Accent.TButton'
        )
        search_btn.grid(row=6, column=0, columnspan=3, pady=15)
        
        # Area risultati
        results_frame = ttk.LabelFrame(main_frame, text="Risultati", padding="15")
        results_frame.pack(fill='both', expand=True)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            height=15
        )
        self.results_text.pack(fill='both', expand=True)
    
    def create_history_tab(self):
        """Crea il tab dello storico prezzi"""
        main_frame = ttk.Frame(self.history_tab, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Form ricerca storico
        form_frame = ttk.LabelFrame(main_frame, text="Seleziona Rotta", padding="15")
        form_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(form_frame, text="Origine:").grid(row=0, column=0, sticky='w', pady=5)
        self.hist_origin_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.hist_origin_var, width=10).grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Destinazione:").grid(row=0, column=2, sticky='w', pady=5, padx=(20, 0))
        self.hist_destination_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.hist_destination_var, width=10).grid(row=0, column=3, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Data Partenza:").grid(row=1, column=0, sticky='w', pady=5)
        self.hist_departure_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.hist_departure_var, width=15).grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(form_frame, text="Data Ritorno:").grid(row=1, column=2, sticky='w', pady=5, padx=(20, 0))
        self.hist_return_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.hist_return_var, width=15).grid(row=1, column=3, pady=5, padx=5)
        ttk.Label(form_frame, text="(opzionale)", foreground='gray').grid(row=1, column=4, sticky='w')
        
        ttk.Button(
            form_frame,
            text="📊 Visualizza Trend",
            command=self.view_price_trend
        ).grid(row=2, column=0, columnspan=5, pady=15)
        
        # Area risultati
        results_frame = ttk.LabelFrame(main_frame, text="Trend Prezzi", padding="15")
        results_frame.pack(fill='both', expand=True)
        
        self.history_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            height=15
        )
        self.history_text.pack(fill='both', expand=True)
    
    def create_routes_tab(self):
        """Crea il tab delle rotte monitorate"""
        main_frame = ttk.Frame(self.routes_tab, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Bottone refresh
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(
            btn_frame,
            text="🔄 Aggiorna Lista",
            command=self.refresh_routes
        ).pack(side='left')
        
        # Area lista rotte
        list_frame = ttk.LabelFrame(main_frame, text="Rotte Monitorate", padding="15")
        list_frame.pack(fill='both', expand=True)
        
        self.routes_text = scrolledtext.ScrolledText(
            list_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            height=20
        )
        self.routes_text.pack(fill='both', expand=True)
        
        # Carica rotte all'avvio
        self.refresh_routes()
    
    def toggle_return_date(self):
        """Abilita/disabilita il campo data ritorno"""
        if self.roundtrip_var.get():
            self.return_entry.config(state='normal')
        else:
            self.return_entry.config(state='disabled')
    
    def search_flights(self):
        """Esegue la ricerca voli"""
        if not self.api_ready:
            messagebox.showerror("Errore", "API non configurata. Controlla il file .env")
            return
        
        # Validazione input
        origin = self.origin_var.get().strip().upper()
        destination = self.destination_var.get().strip().upper()
        departure_date = self.departure_var.get().strip()
        
        if not origin or not destination or not departure_date:
            messagebox.showwarning("Attenzione", "Compila tutti i campi obbligatori")
            return
        
        if len(origin) != 3 or len(destination) != 3:
            messagebox.showwarning("Attenzione", "I codici IATA devono essere di 3 lettere")
            return
        
        return_date = None
        if self.roundtrip_var.get():
            return_date = self.return_var.get().strip()
        
        try:
            adults = int(self.adults_var.get())
        except ValueError:
            messagebox.showwarning("Attenzione", "Numero passeggeri non valido")
            return
        
        # Esegui ricerca in thread separato
        self.status_var.set("⏳ Ricerca in corso...")
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', "⏳ Ricerca voli in corso...\n\n")
        
        thread = threading.Thread(
            target=self._search_flights_thread,
            args=(origin, destination, departure_date, return_date, adults)
        )
        thread.daemon = True
        thread.start()
    
    def _search_flights_thread(self, origin, destination, departure_date, return_date, adults):
        """Thread per la ricerca voli"""
        try:
            if return_date:
                offers = self.client.search_round_trip(
                    origin, destination, departure_date, return_date, adults
                )
            else:
                offers = self.client.search_flights(
                    origin, destination, departure_date, adults
                )
            
            # Salva risultati
            if offers:
                self.storage.save_search(origin, destination, departure_date, return_date, offers)
            
            # Aggiorna UI
            self.root.after(0, self._display_search_results, offers, origin, destination)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Errore", f"Errore nella ricerca: {e}"))
            self.root.after(0, lambda: self.status_var.set("❌ Errore nella ricerca"))
    
    def _display_search_results(self, offers, origin, destination):
        """Visualizza i risultati della ricerca"""
        self.results_text.delete('1.0', tk.END)
        
        if not offers:
            self.results_text.insert('1.0', "❌ Nessun volo trovato per questa rotta.\n")
            self.status_var.set("❌ Nessun risultato")
            return
        
        # Header
        result_text = f"✅ Trovati {len(offers)} voli per {origin} → {destination}\n"
        result_text += "="*80 + "\n\n"
        
        # Volo più economico
        cheapest = min(offers, key=lambda x: x['price']['total'])
        result_text += "🏆 VOLO PIÙ ECONOMICO:\n"
        result_text += f"💰 Prezzo: {cheapest['price']['total']:.2f} {cheapest['price']['currency']}\n\n"
        
        result_text += self._format_flight(cheapest)
        result_text += "\n" + "="*80 + "\n\n"
        
        # Altri voli
        result_text += f"📋 ALTRE OPZIONI ({len(offers)-1} voli):\n\n"
        for idx, offer in enumerate(offers[1:], 2):
            result_text += f"Opzione {idx}: {offer['price']['total']:.2f} {offer['price']['currency']}\n"
            result_text += self._format_flight(offer, brief=True)
            result_text += "\n"
        
        self.results_text.insert('1.0', result_text)
        self.status_var.set(f"✅ Trovati {len(offers)} voli - Risultati salvati")
    
    def _format_flight(self, flight, brief=False):
        """Formatta i dettagli del volo"""
        text = ""
        for idx, itinerary in enumerate(flight['itineraries'], 1):
            if len(flight['itineraries']) > 1:
                text += f"\n{'ANDATA' if idx == 1 else 'RITORNO'}:\n"
            
            if not brief:
                text += f"  Durata totale: {itinerary['duration']}\n"
            
            for seg in itinerary['segments']:
                dep_time = datetime.fromisoformat(seg['departure']['at'].replace('Z', '+00:00'))
                arr_time = datetime.fromisoformat(seg['arrival']['at'].replace('Z', '+00:00'))
                
                text += f"  {seg['departure']['iataCode']} → {seg['arrival']['iataCode']} "
                text += f"({seg['carrier']}{seg['flight_number']})\n"
                
                if not brief:
                    text += f"    Partenza: {dep_time.strftime('%d/%m/%Y %H:%M')}\n"
                    text += f"    Arrivo: {arr_time.strftime('%d/%m/%Y %H:%M')}\n"
        
        return text
    
    def view_price_trend(self):
        """Visualizza il trend prezzi"""
        origin = self.hist_origin_var.get().strip().upper()
        destination = self.hist_destination_var.get().strip().upper()
        departure_date = self.hist_departure_var.get().strip()
        return_date = self.hist_return_var.get().strip() or None
        
        if not origin or not destination or not departure_date:
            messagebox.showwarning("Attenzione", "Compila almeno Origine, Destinazione e Data Partenza")
            return
        
        trend = self.storage.get_price_trend(origin, destination, departure_date, return_date)
        
        self.history_text.delete('1.0', tk.END)
        
        if not trend['found']:
            self.history_text.insert('1.0', f"❌ {trend['message']}\n\nEffettua prima una ricerca per questa rotta.")
            return
        
        # Formato output
        result_text = f"📈 TREND PREZZI\n"
        result_text += f"Rotta: {origin} → {destination}\n"
        result_text += f"Partenza: {departure_date}\n"
        if return_date:
            result_text += f"Ritorno: {return_date}\n"
        result_text += "="*80 + "\n\n"
        
        result_text += f"📊 STATISTICHE:\n"
        result_text += f"  Ricerche effettuate: {trend['searches_count']}\n"
        result_text += f"  Prima ricerca: {self._format_datetime(trend['first_search'])}\n"
        result_text += f"  Ultima ricerca: {self._format_datetime(trend['last_search'])}\n\n"
        
        result_text += f"💰 PREZZI:\n"
        result_text += f"  Prezzo più basso: {trend['lowest_price']:.2f} {trend['currency']}\n"
        result_text += f"  Prezzo più alto: {trend['highest_price']:.2f} {trend['currency']}\n"
        result_text += f"  Prezzo medio: {trend['average_price']:.2f} {trend['currency']}\n"
        result_text += f"  Prezzo attuale: {trend['current_price']:.2f} {trend['currency']}\n\n"
        
        if trend['price_change'] != 0:
            emoji = "📉 SCESO" if trend['price_change'] < 0 else "📈 SALITO"
            result_text += f"📊 VARIAZIONE: {emoji} di {abs(trend['price_change']):.2f} {trend['currency']}\n"
        else:
            result_text += "📊 VARIAZIONE: Nessuna variazione\n"
        
        self.history_text.insert('1.0', result_text)
    
    def refresh_routes(self):
        """Aggiorna la lista delle rotte monitorate"""
        routes = self.storage.get_all_routes()
        
        self.routes_text.delete('1.0', tk.END)
        
        if not routes:
            self.routes_text.insert('1.0', "❌ Nessuna rotta monitorata.\n\nEffettua una ricerca per iniziare a tracciare prezzi.")
            return
        
        result_text = f"🗺️  ROTTE MONITORATE ({len(routes)} rotte)\n"
        result_text += "="*80 + "\n\n"
        
        for idx, route_info in enumerate(routes, 1):
            route = route_info['route']
            result_text += f"{idx}. {route['origin']} → {route['destination']}\n"
            result_text += f"   Partenza: {route['departure_date']}"
            if route['return_date']:
                result_text += f" | Ritorno: {route['return_date']}"
            result_text += "\n"
            result_text += f"   Ricerche: {route_info['searches_count']} | "
            result_text += f"Ultimo prezzo: {route_info['last_price']:.2f} EUR\n"
            result_text += f"   Ultima ricerca: {self._format_datetime(route_info['last_search'])}\n\n"
        
        self.routes_text.insert('1.0', result_text)
    
    def _format_datetime(self, dt_string):
        """Formatta datetime per visualizzazione"""
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime('%d/%m/%Y %H:%M')


def main():
    """Avvia l'applicazione GUI"""
    root = tk.Tk()
    app = FlightTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
