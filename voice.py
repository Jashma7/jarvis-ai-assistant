import speech_recognition as sr
import subprocess


def speak(text):
    print("Jarvis:", text)

    safe_text = text.replace("'", "''")

    powershell_command = (
        "Add-Type -AssemblyName System.Speech; "
        "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$speaker.Speak('" + safe_text + "'); "
        "$speaker.Dispose()"
    )

    subprocess.run(
        ["powershell", "-NoProfile", "-Command", powershell_command],
        capture_output=True,
        text=True
    )


def listen():
    recognizer = sr.Recognizer()

    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=8
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:

        command = recognizer.recognize_google(audio)

        print("You:", command)

        return command.lower()

    except sr.UnknownValueError:

        print("I couldn't understand that. Please try again.")
        return ""

    except sr.RequestError:

        print("Speech recognition service is unavailable.")
        return ""