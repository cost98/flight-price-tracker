# ✈️ Flight Price Tracker

Sistema per tracciare e monitorare i prezzi dei voli utilizzando l'API di Amadeus.

## 🚀 Caratteristiche

- 🔍 Ricerca voli con prezzi in tempo reale
- 📊 Storico prezzi per analizzare trend
- 💰 Trova automaticamente il volo più economico
- 🗺️ Monitora multiple rotte
- 💾 Salvataggio automatico dei risultati delle ricerche
- 📈 Analisi trend prezzi con statistiche

## 📋 Prerequisiti

- Python 3.8 o superiore
- Account Amadeus for Developers (gratuito)

## 🛠️ Installazione

### 1. Clona o scarica il progetto

```bash
cd fligth_tracker
```

### 2. Attiva l'ambiente virtuale

L'ambiente virtuale è già configurato in `.venv`. Attivalo:

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.venv\Scripts\activate.bat
```

### 3. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configura le credenziali API

1. Registrati su [Amadeus for Developers](https://developers.amadeus.com/register)
2. Crea una nuova app per ottenere API Key e API Secret
3. Copia il file `.env.example` in `.env`:
   ```bash
   copy .env.example .env
   ```
4. Apri il file `.env` e inserisci le tue credenziali:
   ```
   AMADEUS_API_KEY=tua_api_key_qui
   AMADEUS_API_SECRET=tua_api_secret_qui
   ```

## 🎯 Utilizzo

### Avviare l'applicazione

```bash
python flight_tracker.py
```

### Funzionalità del Menu

**1. 🔍 Cerca voli**
- Inserisci aeroporto di partenza e destinazione (codici IATA, es: FCO, JFK)
- Scegli data di partenza e opzionalmente data di ritorno
- Specifica numero di passeggeri
- Visualizza risultati con il volo più economico
- I risultati vengono salvati automaticamente

**2. 📊 Visualizza storico prezzi**
- Seleziona una rotta già cercata
- Visualizza statistiche:
  - Prezzo più basso/alto trovato
  - Prezzo medio
  - Variazione prezzi nel tempo
  - Numero di ricerche effettuate

**3. 🗺️ Visualizza rotte monitorate**
- Vedi tutte le rotte che hai cercato
- Per ogni rotta: numero di ricerche e ultimo prezzo

## 📁 Struttura del Progetto

```
fligth_tracker/
├── amadeus_client.py      # Client per API Amadeus
├── price_storage.py        # Gestione storico prezzi
├── flight_tracker.py       # Applicazione principale
├── requirements.txt        # Dipendenze Python
├── .env.example           # Template configurazione
├── .env                   # Le tue credenziali (non committare!)
└── price_history.json     # Database locale prezzi (creato automaticamente)
```

## 🌍 Codici Aeroporto IATA Comuni

Alcuni esempi di codici IATA:

### Italia
- **FCO** - Roma Fiumicino
- **CIA** - Roma Ciampino
- **MXP** - Milano Malpensa
- **LIN** - Milano Linate
- **BGY** - Bergamo Orio al Serio
- **VCE** - Venezia Marco Polo
- **NAP** - Napoli
- **BLQ** - Bologna
- **PSA** - Pisa
- **CTA** - Catania

### Internazionali
- **JFK** - New York JFK
- **LHR** - Londra Heathrow
- **CDG** - Parigi Charles de Gaulle
- **BCN** - Barcellona
- **MAD** - Madrid
- **DXB** - Dubai
- **BKK** - Bangkok

[Lista completa codici IATA](https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code)

## 💡 Esempi di Utilizzo

### Ricerca Andata e Ritorno
```
Partenza: FCO (Roma)
Destinazione: JFK (New York)
Data partenza: 2025-07-15
Data ritorno: 2025-07-22
Passeggeri: 2
```

### Solo Andata
```
Partenza: MXP (Milano)
Destinazione: BCN (Barcellona)
Data partenza: 2025-06-10
Andata e ritorno: n
Passeggeri: 1
```

## 📊 Formato Storico Prezzi

I dati vengono salvati in `price_history.json`:

```json
{
  "searches": [
    {
      "timestamp": "2025-12-04T10:30:00",
      "route": {
        "origin": "FCO",
        "destination": "JFK",
        "departure_date": "2025-07-15",
        "return_date": "2025-07-22"
      },
      "cheapest_price": 450.00,
      "average_price": 620.50,
      "offers_count": 10
    }
  ]
}
```

## 🔧 Personalizzazione

### Modificare il numero di risultati

In `amadeus_client.py`, modifica il parametro `max_results`:

```python
def search_flights(self, ..., max_results=10):
```

### Cambiare valuta

Passa il parametro `currency` nelle funzioni di ricerca:

```python
client.search_flights(..., currency='USD')
```

## ⚠️ Limitazioni API

**Account gratuito Amadeus:**
- 2,000 chiamate API al mese
- Dati in tempo reale
- Nessun costo

Per più dettagli: [Amadeus Pricing](https://developers.amadeus.com/pricing)

## 🐛 Troubleshooting

**Errore "AMADEUS_API_KEY not configured"**
- Assicurati di aver creato il file `.env`
- Verifica che le credenziali siano corrette

**Errore "No flights found"**
- Verifica i codici aeroporto IATA
- Controlla che la data sia in formato YYYY-MM-DD
- Assicurati che la data sia futura

**ResponseError dall'API**
- Controlla di avere crediti API disponibili
- Verifica la connessione internet
- Consulta [Amadeus Documentation](https://developers.amadeus.com/docs)

## 📚 Risorse

- [Amadeus API Documentation](https://developers.amadeus.com/docs)
- [Amadeus Python SDK](https://github.com/amadeus4dev/amadeus-python)
- [IATA Airport Codes](https://www.iata.org/en/publications/directories/code-search/)

## 📝 Note

- I prezzi possono variare rapidamente
- Effettua ricerche regolari per tracciare trend
- I dati sono salvati localmente in `price_history.json`
- Non condividere il file `.env` con le tue credenziali

## 🤝 Contributi

Sentiti libero di migliorare il progetto! Alcune idee:
- Aggiungere notifiche email quando i prezzi scendono
- Creare grafici per visualizzare trend prezzi
- Integrare altre API di voli
- Creare interfaccia web con Flask/Django

## 📄 Licenza

Questo progetto è fornito "as-is" per scopi educativi.

---

Buon tracking! ✈️💰
