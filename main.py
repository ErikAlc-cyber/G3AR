"""
Copyright (C) 2020  Erik Alcantara Covarrubias email: erik.senseya@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.en.html.
"""
from __future__ import print_function

import numpy as np
import subprocess
import speech_recognition as sr
import time
import simpleaudio as sa
import pyttsx3 as pt3
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

""""Activa el microfono / Activates the microphone"""
mic = sr.Microphone()

""""Reconocer la voz / Recongnice the voice"""
audio = sr.Recognizer()

"""
    Mensaje de bienvenida / welcome message
"""
wave_obj = sa.WaveObject.from_wave_file("Animaker Voice.wav")
play_obj = wave_obj.play()
play_obj.wait_done()

# ######################################################################################################################################################################################

"""
Configurar la assistente / Configurate the voice
"""


def speak(text):
    engine = pt3.init()  # Inicia la voz / starts the voice
    """
   Este es la voz, idioma y si es mujer o hombre / this is the voice, the language and if it's male or female
   """
    voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    engine.setProperty('voice', voice)
    engine.setProperty('volume', 0.8)  # volumen / volume
    engine.setProperty('rate', 85)  # velocidad / speed
    engine.say(text)
    engine.runAndWait()


def hear(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audioin = recognizer.listen(source)
        user = recognizer.recognize_google(
            audioin)  # Select the desire languaje / Selecciona el idioma que hablas: language='fr-FR / en-US / en-UK / es-US'
    print(user)
    return user.lower()


def talk():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    trans = hear(recognizer, microphone)

    if trans in ['exit']:
        speak("Ok, see you later")
        exit()

    elif trans in ['save']:
        speak('Tell me what you want to save')
        file = hear(recognizer, microphone)
        save_file(file)
        speak("Done, thank you")

    #    elif trans in ['open']:
    #        open_file()

    elif trans in ['repeat']:
        speak('Tell me what you want to repeat')
        rep = hear(recognizer, microphone)
        print(rep)
        speak("Ok")
        speak(rep)

    elif trans in ['time']:  # time / tiempo
        speak("the date and time is" + time.ctime())

    elif trans in ['open']:
        speak("What do you want to open?")
        exe = hear(recognizer, microphone)
        openexe(exe)

    elif trans in ['cmd']:
        speak("ok, try to not ruin windows please")
        ComandLine()

    elif trans in ['calendar']:
        speak("ok, what day?")
        n = hear(recognizer, microphone)
        print(n)
        date = get_date(n)
        if date:
            get_events(date, service)
        else:
            speak('I dont understand, please repeat')

    elif trans in ["note"]:
        speak("What do you want to remember")
        text = hear(recognizer, microphone)
        note(text)

    elif trans:
        speak('I dont understand, please repeat')


"""Abre los mensajes / Open the notes"""

"""
def open_file():
    '''abre un archivo / opens a file'''
    fichero = open("Notas.txt", 'r')
    contenido = fichero.readlines()
    print(contenido)
    talk(contenido)
"""

"""Guarda el mensaje / Saves the files"""


def save_file(trans):
    """Salve el archivo / saves a file"""
    date = time.ctime()
    ruta = str(date).replace(":", "-") + "~note.txt"
    contenido = trans
    fichero = open(ruta, 'w')
    # fichero.write("\""+contenido+"\"")
    fichero.write(contenido)
    fichero.close()


"""La funcion principal / Main function"""


def openexe(exe):
    subprocess.Popen([exe + ".exe"])


def ComandLine():
    # Define command as string / Define el comando como un string
    cmd = 'help'
    # Use shell to execute the command and store it in sp variable / Usa CMD para ejecutar el comando y lo guarda en sp
    sp = subprocess.Popen(cmd, shell=True)
    # Store the return code in rc variable / Se guarda la respuesta en rc
    rc = sp.wait()
    # Print the content of sp variable / Se imprime sp
    print(sp)
    print(rc)


def Main_loop():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    wake = "hey assistant"
    while True:
        text = hear(recognizer, microphone)
        if text.count(wake) > 0:
            speak("I am ready")
            talk()
            speak('Anything else you want me to do?')
            Main_loop()


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(date, service):
    # Call the Calendar API
    date = datetime.datetime.combine(date, datetime.datetime.min.time())
    end = datetime.datetime.combine(date, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end = end.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak(print('No upcoming events found.'))
    else:
        speak(f"You have {len(events)} events on this today")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(":")[1]
                start_time = start_time + "pm"

            speak(event["summary"] + "at" + start_time)


# noinspection PyBroadException
def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1

        elif word in DAYS:
            day_week = DAYS.index(word)

        elif word.isdigit():
            day = int(word)

        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if day < today.day and month == -1 and day != -1:
        month = month + 1

    if month == -1 and today == -1 and day_week != -1:
        current_day_week = today.weekday()
        dif = day_week - current_day_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        return today + datetime.timedelta(dif)

    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "~note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


# #############################################################################################################################################################################################


"""Begin the actual program / aqui empieza el programa"""

service = authenticate_google()
Main_loop()
