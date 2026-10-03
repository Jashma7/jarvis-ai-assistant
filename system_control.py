import webbrowser
import datetime
import subprocess


def open_youtube():
    webbrowser.open("https://www.youtube.com")


def open_google():
    webbrowser.open("https://www.google.com")


def google_search(query):
    search_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(search_url)


def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return current_time


def open_calculator():
    subprocess.Popen("calc.exe")