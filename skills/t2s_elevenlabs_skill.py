# t2s_elevenlabs_skill.py

import os
import requests
import pygame
import time
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

# ElevenLabs API-Key und Voice-ID aus Umgebungsvariablen laden
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# Text-to-speech Funktion
def spreche_text(text):
    if text:
        # Entferne die Zeichen `` aus dem Text
        bereinigter_text = text.replace("`", "")
        
        # API-Anfrage zur Text-zu-Sprache Umwandlung
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        data = {
            "text": bereinigter_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.7,
                "similarity_boost": 0.6
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Temporäre MP3-Datei speichern
            temp_file = "antwort.mp3"
            with open(temp_file, "wb") as audio_file:
                audio_file.write(response.content)
            
            # Lade und spiele die Audiodatei ab
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Warten, bis das Abspielen abgeschlossen ist
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Warten Sie kurz, bevor Sie die Datei löschen
            time.sleep(1)
            
            # Mixer beenden und Datei entfernen
            pygame.mixer.quit()
            os.remove(temp_file)
        else:
            print(f"Fehler bei der API-Anfrage von ElevenLabs: {response.status_code}")
            print(response.text)
    else:
        print("Keine Antwort zum Sprechen")