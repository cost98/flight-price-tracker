# 🚀 Deploy Guide - Flight Price Tracker

## Opzioni di Deploy Gratuito

### 1. Render.com (Consigliato ⭐)

**Vantaggi:**
- ✅ Tier gratuito generoso (750 ore/mese)
- ✅ SSL automatico
- ✅ Deploy da GitHub automatico
- ✅ Supporto variabili d'ambiente

**Passi:**

1. **Prepara il repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Crea repository su GitHub:**
   - Vai su https://github.com/new
   - Crea un nuovo repository
   - Pusha il codice:
   ```bash
   git remote add origin https://github.com/TUO_USERNAME/flight-tracker.git
   git push -u origin main
   ```

3. **Deploy su Render:**
   - Vai su https://render.com
   - Registrati (gratis)
   - Click "New +" → "Web Service"
   - Connetti il tuo repository GitHub
   - Configurazione:
     - **Name**: flight-tracker
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   - Aggiungi variabili d'ambiente:
     - `AMADEUS_API_KEY`: la tua chiave
     - `AMADEUS_API_SECRET`: il tuo secret
   - Click "Create Web Service"

4. **URL finale:**
   - `https://flight-tracker-xxxx.onrender.com`

**Nota:** Il tier gratuito va in sleep dopo 15 minuti di inattività (primo caricamento lento).

---

### 2. Railway.app

**Vantaggi:**
- ✅ Deploy semplicissimo
- ✅ $5 gratis al mese
- ✅ Molto veloce

**Passi:**
1. Vai su https://railway.app
2. Registrati con GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Seleziona il repository
5. Aggiungi variabili d'ambiente
6. Deploy automatico!

---

### 3. PythonAnywhere

**Vantaggi:**
- ✅ Sempre attivo (no sleep)
- ✅ Facile per principianti
- ✅ Console web

**Passi:**
1. Registrati su https://www.pythonanywhere.com
2. Vai su "Web" → "Add a new web app"
3. Scegli Flask
4. Upload dei file via console o Git
5. Configura variabili d'ambiente nel file WSGI

---

### 4. Vercel (con adattatore)

**Vantaggi:**
- ✅ Velocissimo
- ✅ Deploy automatico da Git
- ✅ Edge network globale

**Limitazioni:**
- ⚠️ Funzioni serverless (richiede adattamento)

---

### 5. Heroku (Limitato)

**Nota:** Heroku ha rimosso il tier gratuito, ora richiede carta di credito.

---

## 📝 Checklist Prima del Deploy

- [x] File `Procfile` creato
- [x] `gunicorn` aggiunto a requirements.txt
- [x] `runtime.txt` con versione Python
- [ ] `.env` aggiunto a `.gitignore` (già fatto)
- [ ] Credenziali API configurate sul server (non commitarle!)
- [ ] Repository Git inizializzato
- [ ] Codice pushato su GitHub

---

## 🔒 Sicurezza

**IMPORTANTE:** Non committare mai il file `.env` con le credenziali!

Le credenziali vanno configurate come **variabili d'ambiente** sulla piattaforma di hosting.

---

## 🎯 Raccomandazione Finale

**Per questo progetto → Render.com**

Motivi:
- Gratuito e affidabile
- Supporto Python/Flask nativo
- Facile gestione variabili d'ambiente
- Deploy automatico da GitHub
- SSL incluso

---

## 🚀 Quick Deploy con Render

```bash
# 1. Installa gunicorn localmente
pip install gunicorn

# 2. Inizializza Git
git init
git add .
git commit -m "Ready for deployment"

# 3. Pusha su GitHub
git remote add origin https://github.com/TUO_USERNAME/flight-tracker.git
git push -u origin main

# 4. Vai su render.com e connetti il repo
# 5. Aggiungi le variabili d'ambiente
# 6. Deploy! 🎉
```

Il tuo Flight Price Tracker sarà online in 5 minuti! ✈️
