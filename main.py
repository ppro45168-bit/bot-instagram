import os
import requests
import time

# --- CONFIGURAZIONE ---
IG_USER_ID = os.environ.get("IG_USER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

# URL DI UN VIDEO MP4 PUBBLICO (Per il test usiamo questo coniglio)
VIDEO_URL = "https://www.w3schools.com/html/mov_bbb.mp4"
DIDASCALIA = "Test Reel automatico! 🐰 #bot #python #coding"

def pubblica_reel():
    print("------------------------------------------------")
    print("🎬 AVVIO PUBBLICAZIONE REEL...")
    
    # PASSO 1: Carichiamo il Video
    # Nota: Qui specifichiamo 'media_type': 'REELS'
    url_container = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        "video_url": VIDEO_URL,
        "caption": DIDASCALIA,
        "media_type": "REELS", 
        "access_token": ACCESS_TOKEN
    }
    
    print("Caricamento video sui server Meta in corso...")
    r = requests.post(url_container, data=payload)
    
    if r.status_code != 200:
        print("❌ ERRORE CARICAMENTO:", r.text)
        return

    creation_id = r.json().get("id")
    print(f"✅ Video caricato! ID: {creation_id}")
    
    # IMPORTANTE: I video ci mettono tempo a essere elaborati.
    # Aspettiamo 45 secondi per essere sicuri.
    print("⏳ Attendo 45 secondi che Instagram elabori il video...")
    time.sleep(45)

    # PASSO 2: Pubblichiamo
    url_publish = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    payload_pub = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    
    print("🚀 Pubblicazione finale...")
    r_pub = requests.post(url_publish, data=payload_pub)
    
    if r_pub.status_code == 200:
        print("🎉 REEL PUBBLICATO! VAI A VEDERE!")
    else:
        print("❌ ERRORE PUBBLICAZIONE (Forse serviva più tempo?):", r_pub.text)
    print("------------------------------------------------")

if __name__ == "__main__":
    pubblica_reel()
    while True:
        time.sleep(60)
