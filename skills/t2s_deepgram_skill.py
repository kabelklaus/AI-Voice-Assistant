# t2s_deepgram_skill.py

import os
import pygame
import time
from dotenv import load_dotenv
from deepgram import DeepgramClient, SpeakOptions

# Lade Umgebungsvariablen
load_dotenv()

# Deepgram API-Key aus Umgebungsvariablen laden
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Initialisiere den Deepgram Client
deepgram = DeepgramClient(api_key=DEEPGRAM_API_KEY)

# Text-to-speech Funktion
def spreche_text(text):
    if text:
        # Entferne die Zeichen `` aus dem Text
        bereinigter_text = text.replace("`", "")
        
        # Konfiguriere die Speak-Optionen
        options = SpeakOptions(
            model="aura-asteria-en",  # Verwende das englische Modell
            encoding="mp3",  # Wir verwenden MP3 für die Kompatibilität mit dem vorhandenen Code
        )

        try:
            # Temporäre MP3-Datei
            temp_file = "antwort.mp3"
            
            # API-Anfrage zur Text-zu-Sprache Umwandlung und Speichern der Datei
            response = deepgram.speak.v("1").save(temp_file, {"text": bereinigter_text}, options)
            
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
            
            # Ausgabe der Responsedaten
            print(f"Text-to-Speech erfolgreich durchgeführt.")
            print(f"Verwendetes Modell: {options.model}")
            print(f"Anzahl der Zeichen: {len(bereinigter_text)}")
            
        except Exception as e:
            print(f"Fehler bei der Verarbeitung durch Deepgram: {str(e)}")
    else:
        print("Keine Antwort zum Sprechen")