import os
import requests
import time

# --- CONFIGURAZIONE ---
IG_USER_ID = os.environ.get("IG_USER_ID")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
# Immagine di prova (un paesaggio generico)
FOTO_TEST = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80"
DIDASCALIA = "Ciao! Questa è la prima prova automatica dal mio Bot 🚀"

def pubblica_foto():
    print("------------------------------------------------")
    print("AVVIO PROCEDURA DI PUBBLICAZIONE...")
    
    # PASSO 1: Carichiamo la foto sui server di Facebook
    url_container = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    payload = {
        "image_url": FOTO_TEST,
        "caption": DIDASCALIA,
        "access_token": ACCESS_TOKEN
    }
    
    print("Creazione del contenitore media...")
    r = requests.post(url_container, data=payload)
    
    if r.status_code != 200:
        print("❌ ERRORE NEL CARICAMENTO:", r.text)
        return

    creation_id = r.json().get("id")
    print(f"✅ Contenitore creato! ID: {creation_id}")
    
    # Aspettiamo un attimo che Facebook elabori la foto
    time.sleep(5) 

    # PASSO 2: Pubblichiamo ufficialmente
    url_publish = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    payload_pub = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }
    
    print("Pubblicazione in corso...")
    r_pub = requests.post(url_publish, data=payload_pub)
    
    if r_pub.status_code == 200:
        print("🚀 FOTO PUBBLICATA CON SUCCESSO! CONTROLLA INSTAGRAM!")
    else:
        print("❌ ERRORE NELLA PUBBLICAZIONE:", r_pub.text)
    print("------------------------------------------------")

if __name__ == "__main__":
    pubblica_foto()
    # Questo ciclo serve a non far spegnere subito il bot su Railway
    while True:
        time.sleep(60)
