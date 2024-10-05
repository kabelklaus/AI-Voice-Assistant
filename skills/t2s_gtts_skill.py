# t2s_gtts_skill.py

import os
from gtts import gTTS
import pygame
import time

# Text-to-speech function
def spreche_text(text):
    if text:
        # Entferne die Zeichen `` aus dem Text
        bereinigter_text = text.replace("`", "")
        
        # Konvertiere den bereinigten Text in Sprache
        tts = gTTS(text=bereinigter_text, lang="de")
        dateiname = "antwort.mp3"
        tts.save(dateiname)
        
        # Lade und spiele die Audiodatei ab
        pygame.mixer.init()
        pygame.mixer.music.load(dateiname)
        pygame.mixer.music.play()
        
        # Warten, bis das Abspielen abgeschlossen ist
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
        
        # Warten Sie kurz, bevor Sie die Datei löschen
        time.sleep(1)
        
        # Mixer beenden und Datei entfernen
        pygame.mixer.quit()
        os.remove(dateiname)
    else:
        print("Keine Antwort zum Sprechen")
