# s2t_skill.py

import speech_recognition as sr

def get_audio_input():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Bitte sprechen Sie jetzt...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ich höre zu...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Spracherkennung läuft...")
        except sr.WaitTimeoutError:
            print("Es wurde keine Sprache erkannt. Bitte versuchen Sie es erneut.")
            return None
    
    try:
        text = recognizer.recognize_google(audio, language="de-DE")
        print(f"Erkannter Text: {text}")
        return text
    except sr.UnknownValueError:
        print("Entschuldigung, ich konnte Sie nicht verstehen.")
        return None
    except sr.RequestError as e:
        print(f"Fehler bei der Anfrage an den Spracherkennungsdienst: {e}")
        return None

def continuous_audio_input():
    while True:
        result = get_audio_input()
        if result:
            return result
        print("Versuchen Sie es bitte erneut.")