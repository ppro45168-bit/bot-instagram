import os
import requests
import time
import random
import schedule  # <-- AGGIUNTO: Serve per la sveglia

# --- CONFIGURAZIONE ---
IG_USER_ID = os.environ.get("IG_USER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY")

# --- IMPOSTA QUI L'ORARIO DI PUBBLICAZIONE ---
ORARIO_POST = "18:30" 

ARGOMENTI_VIDEO = ["sunset", "nature", "forest", "ocean", "road trip", "mountains"]

FRASI_MOTIVAZIONALI = [
    "Non smettere mai di sognare, solo chi sogna può volare. ✨",
    "Il successo è la somma di piccoli sforzi, ripetuti giorno dopo giorno.",
    "Non aspettare il momento giusto, crealo.",
    "La disciplina ti porterà dove la motivazione non può arrivare. 🚀",
    "Sii la versione migliore di te stesso.",
    "Ogni giorno è una nuova opportunità per ricominciare.",
    "Non guardare indietro, non è lì che stai andando.",
    "Il fallimento è solo un passo verso il successo.",
    "Lavora in silenzio, lascia che sia il tuo successo a fare rumore.",
    "La tua unica competizione è chi eri ieri.",
    "Se puoi sognarlo, puoi farlo.",
    "La calma è la virtù dei forti.",
    "Respira. È solo una brutta giornata, non una brutta vita.",
    "Le cose belle richiedono tempo. Abbi pazienza.",
    "Non conta quanto vai piano, l'importante è non fermarsi.",
    "Il tuo unico limite è la tua mente. Rompi gli schemi. 🧠✨",
    "Non aver paura di fallire, abbi paura di non averci provato.",
    "Costruisci i tuoi sogni o qualcuno ti assumerà per costruire i suoi. 🏗️",
    "La costanza batte il talento quando il talento non si impegna.",
    "Sii la voce, non l'eco. 🗣️",
    "Grandi traguardi richiedono grandi ambizioni.",
    "Il segreto per andare avanti è iniziare. 🚀",
    "Fai oggi ciò che gli altri non faranno, per vivere domani come gli altri non potranno.",
    "La mente è come un paracadute: funziona solo se si apre. 🪂",
    "Trasforma le tue ferite in saggezza.",
    "Non sognare la tua vita, vivi il tuo sogno. 🌟",
    "L'eccellenza non è un atto, ma un'abitudine.",
    "Il successo non è la chiave della felicità, la felicità è la chiave del successo.",
    "Cadi sette volte, rialzati otto. 🔄",
    "Le persone che dicono che non si può fare non dovrebbero interrompere chi lo sta facendo."
]

def trova_video_pexels():
    argomento = random.choice(ARGOMENTI_VIDEO)
    print(f"🔎 Cerco un video su Pexels a tema: {argomento}...")
    url = f"https://api.pexels.com/videos/search?query={argomento}&per_page=20&orientation=portrait"
    headers = {"Authorization": PEXELS_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data = r.json()
        videos = data.get("videos", [])
        if len(videos) > 0:
            video_scelto = random.choice(videos)
            video_files = video_scelto.get("video_files", [])
            video_files.sort(key=lambda x: x['width'], reverse=True)
            for vid in video_files:
                if vid['width'] <= 1080:
                    print(f"✅ Video trovato! ID: {video_scelto['id']}")
                    return vid['link']
            return video_files[0]['link']
    return None

# --- QUESTA FUNZIONE FA IL LAVORO VERO E PROPRIO ---
def avvia_pubblicazione():
    print(f"⏰ {time.strftime('%H:%M:%S')} - Inizio procedura automatica...")
    link = trova_video_pexels()
    if not link:
        print("❌ Video non trovato, riprovo al prossimo ciclo.")
        return

    frase_del_giorno = random.choice(FRASI_MOTIVAZIONALI)
    didascalia_completa = f"{frase_del_giorno}\n\n.\n.\n#motivazione #ispirazione #mindset #successo"

    print("🎬 AVVIO PUBBLICAZIONE...")
    url_container = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {"video_url": link, "caption": didascalia_completa, "media_type": "REELS", "access_token": ACCESS_TOKEN}
    
    r = requests.post(url_container, data=payload)
    if r.status_code == 200:
        creation_id = r.json().get("id")
        print(f"✅ Container creato! ID: {creation_id}. Attendo 60s...")
        time.sleep(60)
        
        url_publish = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
        r_pub = requests.post(url_publish, data={"creation_id": creation_id, "access_token": ACCESS_TOKEN})
        if r_pub.status_code == 200:
            print("🎉 REEL PUBBLICATO CON SUCCESSO!")
        else:
            print("❌ ERRORE PUBBLICAZIONE:", r_pub.text)
    else:
        print("❌ ERRORE CARICAMENTO:", r.text)

# --- IL CUORE DEL BOT CHE GESTISCE IL TEMPO ---
if __name__ == "__main__":
    print(f"🤖 Bot Online! Orario programmato: {ORARIO_POST}")
    
    # Programma l'azione ogni giorno
    schedule.every().day.at(ORARIO_POST).do(avvia_pubblicazione)

    while True:
        schedule.run_pending()
        time.sleep(30) # Controlla ogni 30 secondi se è l'ora giusta
