import os
import time
import requests

# Legge le chiavi da Railway
ig_user_id = os.environ.get("IG_USER_ID")
access_token = os.environ.get("ACCESS_TOKEN")

print("------------------------------------------------")
print("BOT AVVIATO CORRETTAMENTE!")
print(f"Sto usando l'ID Instagram: {ig_user_id}")
print("Se vedi questo messaggio, Railway funziona.")
print("------------------------------------------------")

# Questo ciclo tiene il bot "sveglio" all'infinito
while True:
    time.sleep(60)
