# t2s_openai_skill.py

import os
import pygame
import time
from dotenv import load_dotenv
from openai import OpenAI

# Lade Umgebungsvariablen
load_dotenv()

# OpenAI API-Key aus Umgebungsvariablen laden
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialisiere den OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

# Text-to-speech Funktion
def spreche_text(text):
    if text:
        # Entferne die Zeichen `` aus dem Text
        bereinigter_text = text.replace("`", "")
        
        try:
            # API-Anfrage zur Text-zu-Sprache Umwandlung
            response = client.audio.speech.create(
                model="tts-1",
                voice="echo",  # Du kannst die Stimme hier anpassen
                input=bereinigter_text
            )
            
            # Temporäre MP3-Datei
            temp_file = "antwort.mp3"
            
            # Speichere die Audiodatei
            response.stream_to_file(temp_file)
            
            # Lade und spiele die Audiodatei ab
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Warten, bis das Abspielen abgeschlossen ist
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(1)
            
            # Warten Sie kurz, bevor Sie die Datei löschen
            time.sleep(1)
            
            # Mixer beenden und Datei entfernen
            pygame.mixer.quit()
            os.remove(temp_file)
            
        except Exception as e:
            print(f"Fehler bei der Verarbeitung durch OpenAI: {str(e)}")
    else:
        print("Keine Antwort zum Sprechen")