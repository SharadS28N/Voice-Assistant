import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import requests
from gtts import gTTS
import time

chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\nAssistant: "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": chatStr},
        ],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    reply = response["choices"][0]["message"]["content"]
    say(reply)
    chatStr += f"{reply}\n"
    return reply

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    reply = response["choices"][0]["message"]["content"]
    say(reply)
    text += reply
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    tts = gTTS(text=text, lang='en')
    tts.save("temp.mp3")
    os.system("mpg123 temp.mp3")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Some Error Occurred: ", e)
            return "Some Error Occurred. Sorry from Aleo"

def getDefinition(term):
    url = f"https://api.dictionaryapi.dev/api/v3/references/thesaurus/json/{term}"
    response = requests.get(url)
    data = response.json()
    if data and 'meanings' in data[0]:
        return data[0]['meanings'][0]['definitions'][0]['definition']
    else:
        return "No definition found for the given term."

if __name__ == '__main__':
    print('Welcome to Aleo')
    say("Hey there, I am Aleo! How May I Help you?")
    while True:
        query = takeCommand().lower()
        if "open youtube" in query:
            say("Opening YouTube sir...")
            webbrowser.open("https://www.youtube.com")
        elif "open wikipedia" in query:
            say("Opening Wikipedia sir...")
            webbrowser.open("https://www.wikipedia.com")
        elif "open google" in query:
            say("Opening Google sir...")
            webbrowser.open("https://www.google.com")
        elif "open music" in query:
            musicPath = "/src/music.mp3"
            os.system(f"open {musicPath}")
        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"The current time is {hour} hours and {minute} minutes sir")
        elif "definition of" in query:
            term = query.split("definition of")[1].strip()
            say(getDefinition(term))
        elif "who are you" in query:
            say("I am Aleo, your AI friend and I am here to assist you in your tasks")
        elif "exit" in query:
            break
        else:
            try:
                chat(query)
            except Exception as e:
                say("Some error occurred while processing your query. Please try again.")
        time.sleep(1)
