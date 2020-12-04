"""
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   print(voice.id)
   engine.say('Here we go round the mulberry bush.')
engine.runAndWait()



def speak(text):
   engine = pyttsx3.init()
   engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
   engine.say(text)
   engine.runAndWait()


def open_file():
   ruta = "Notas.txt"

   fichero = open(ruta, 'r')
   contenido = fichero.readlines()
   print(contenido)
   speak(contenido)

open_file()

import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()
sr.Microphone.list_microphone_names()
"""
""" 
from playsound import playsound

playsound('Ecatepec_Manuel.mp3')
"""
import subprocess

# Define command as string
cmd = "ls -ltr"

# Use shell to execute the command and store it in sp variable
sp = subprocess.Popen(cmd,shell=True)

# Store the return code in rc variable
rc=sp.wait()

# Print the content of sp variable
print(sp)