import os
import requests
import time
import random

# --- CONFIGURAZIONE ---
IG_USER_ID = os.environ.get("IG_USER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY")

# COSA DEVE CERCARE IL BOT? (Cambia questa parola come vuoi)
ARGOMENTO = "nature"  # Prova: "cars", "sunset", "city", "cats"
DIDASCALIA = f"Wonderful {ARGOMENTO} vibes! ✨ #reel #{ARGOMENTO} #vibes"

def trova_video_pexels():
    print(f"🔎 Cerco un video su Pexels: {ARGOMENTO}...")
    
    url = f"https://api.pexels.com/videos/search?query={ARGOMENTO}&per_page=15&orientation=portrait"
    headers = {"Authorization": PEXELS_KEY}
    
    r = requests.get(url, headers=headers)
    
    if r.status_code == 200:
        data = r.json()
        videos = data.get("videos", [])
        
        if len(videos) > 0:
            # Ne prendiamo uno a caso tra i 15 trovati
            video_scelto = random.choice(videos)
            
            # Cerchiamo il file video MP4 con la qualità migliore per Instagram
            video_files = video_scelto.get("video_files", [])
            # Ordiniamo per larghezza per trovare una buona qualità ma non eccessiva
            video_files.sort(key=lambda x: x['width'], reverse=True)
            
            link_video = video_files[0]['link']
            print(f"✅ Video trovato! ID Pexels: {video_scelto['id']}")
            return link_video
        else:
            print("❌ Nessun video trovato.")
            return None
    else:
        print("❌ Errore Pexels:", r.text)
        return None

def pubblica_reel(video_url):
    if not video_url:
        return

    print("------------------------------------------------")
    print("🎬 AVVIO PUBBLICAZIONE REEL AUTOMATICO...")
    
    # PASSO 1: Carichiamo il Video
    url_container = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        "video_url": video_url,
        "caption": DIDASCALIA,
        "media_type": "REELS", 
        "access_token": ACCESS_TOKEN
    }
    
    print("Caricamento sui server Meta...")
    r = requests.post(url_container, data=payload)
    
    if r.status_code != 200:
        print("❌ ERRORE CARICAMENTO META:", r.text)
        return

    creation_id = r.json().get("id")
    print(f"✅ Container creato! ID: {creation_id}")
    
    # I video di Pexels sono pesanti, diamo tempo a Instagram
    print("⏳ Attendo 60 secondi per l'elaborazione...")
    time.sleep(60)

    # PASSO 2: Pubblichiamo
    url_publish = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    payload_pub = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    
    print("🚀 Pubblicazione finale...")
    r_pub = requests.post(url_publish, data=payload_pub)
    
    if r_pub.status_code == 200:
        print("🎉 REEL PUBBLICATO! Il bot ha fatto tutto da solo.")
    else:
        print("❌ ERRORE PUBBLICAZIONE:", r_pub.text)
    print("------------------------------------------------")

if __name__ == "__main__":
    # 1. Trova il video
    link = trova_video_pexels()
    
    # 2. Pubblica
    if link:
        pubblica_reel(link)
    
    # Mantieni attivo
    while True:
        time.sleep(60)
