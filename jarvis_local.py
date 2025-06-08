# i have the python file on my desktop
# on the terminal of your machine
# use "cd Desktop"
# then use "python *python file*
# program should run on terminal
# and will only run on the terminal
# improvements will come and new features will be added
# this will only work offline as using an open.ai requires me to pay

# you'll need to install these packages onto your terminal before they work here
# for mac, i used these
# pip install openai
# pip install pyttsx3
# pip install SpeechRecognition
# pip install pyaudio

import pyttsx3, queue
import os
import sounddevice as sd
import vosk, json
import webbrowser, subprocess
import datetime
import platform
import spotipy

# this is to initialize spotify
# spotify stuff down here
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    # add your own client id if you want to use this
    client_id = "",
    # add your own client secret if you want to use this
    client_secret = "",
    # find the uri that works for you
    redirect_uri = "",
    scope = "user-modify-playback-state,user-read-playback-state"
))


def play_spotify():
    speak("Attempting to play your playlist.")
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        # add your own client id if you want to use this
        client_id = "",
        # add your own client secret if you want to use this
        client_secret = "",
        # find the uri that works for you
        redirect_uri = "",
        scope = "user-read-playback-state user-modify-playback-state"
    ))

    devices = sp.devices()
    if not devices['devices']:
        speak("No active Spotify device found. Please open Spotify and play a song manually first.")
        return

    # enter your playlist uri after the colon
    playlist_uri = "spotify:playlist:"
    sp.start_playback(context_uri = playlist_uri)



# voice things down here

engine = pyttsx3.init()

voices = engine.getProperty('voices')
# list of voices that are possible

engine.setProperty('voice', voices[132].id)
# personal list of my favorites
# 82 Karen
# 132 Samantha
# 164 Tessa

for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.name} ({voice.id})")
tts = pyttsx3.init()
# i think 190 sound fine
# but that's a personal preference
# change it to speed or slow it down
tts.setProperty('rate', 190)

def speak(text):
    # this will be returned on the terminal
    print("SAM: ", text)
    #Super Assisting Mate - SAM
    tts.say(text)
    tts.runAndWait()

model = vosk.Model("model")
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# this will say the date
def tell_date():
    today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today is {today}.")

# this will open apps
# these are set up to work for macbook
# windows needs a different format to open up links
def open_app(app_name):
    if "chrome" in app_name:
        speak("Opening Google Chrome.")
        os.system("open -a 'Google Chrome'")
    elif "calculator" in app_name:
        speak("Opening Calculator.")
        os.system("open -a Calculator")
    elif "textedit" in app_name or "notepad" in app_name:
        speak("Opening TextEdit.")
        os.system("open -a TextEdit")
    else:
        speak("I couldn't find that application, sir.")

# this should do math
def do_math(query):
    try:
        result = eval(query)
        speak(f"The answer is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

# this should open websites
# add more as you please
def open_website(site_name):
    urls = {
        "youtube": "https://youtube.com",
        "google": "https://google.com",
        "indeed": "https://indeed.com"
    }

    for name in urls:
        if name in site_name:
            speak(f"Opening {name}")
            webbrowser.open(urls[name])
            return
        speak("I don't know that site.")

# this opens discord
def open_discord():
    speak("Opening Discord.")
    # change this format if using windows
    os.system("open -a Discord")


def listen():
    with sd.RawInputStream(samplerate = 16000, blocksize = 8000, dtype = 'int16', channels = 1, callback = callback):
        # when nothing is said, this will be repeated
        print("Talk to me...")
        rec = vosk.KaldiRecognizer(model, 16000)

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "").strip()
            


#basic understanding, can be replaced with smarter logic later    
# will keep updating this
# maybe break in section for more organization?

def respond_to(query):
    query = query.lower()

    # basic commands
    if "hello" in query or "hi" in query:
        speak("At your service, sir.")
    elif "your name" in query:
        speak("I am your Super Assisting Mate, but you can call me SAM, sir.")
    elif "my name" in query:
        # enter your name unless your name is also Ryan
        speak("You are Ryan, my creator, sir.")
    elif "my birthday" in query:
        # enter your own birthday
        speak("")

    # day/dates/times
    elif "time" in query:
        from datetime import datetime
        return f"The time is {datetime.now().strftime('%I:%M %p')}."
    elif "date" in query:
        tell_date()

    # actions
    elif "open" in query:
        if "chrome" in query or "calculator" in query or "spotify" in query:
            open_app(query)
        else:
            speak("Sorry, I can't open that app yet.")
    elif "go to" in query or "open website" in query:
        open_website(query)
    # spotify stuff
    elif "play spotify" in query or "play my playlist" in query:
        play_spotify()
    elif "pause" in query or "stop" in query:
        sp.pause_playback()
        return "Paused playback, sir."
    elif "resume" in query or "play" in query:
        sp.start_playback()
        return "Resuming playback, sir."
    elif "skip" in query or "next" in query:
        sp.next_track()
        return "Skipping to next track, sir."
    elif "previous" in query or "back" in query:
        sp.previous_track()
        return "Going back to previous track, sir."

    # close SAM
    elif "exit" in query or "quit" in query or "goodbye" in query or "by" in query or "good bye" in query:
        speak("Goodbye, sir.")
        exit(0)
    
    #else:
    #    speak("I'm not sure how to help with that, sir.")


# this is the main portion and will loop
# wake word
WAKE_WORD = "hey sam"

if __name__ == "__main__":
    speak("Hello, I am SAM. Say 'Hey SAM' to wake me up, sir.")

    while True:
        user_input = listen()
        print("You said:", user_input)

        if not user_input:
            continue

        user_input = user_input.lower().strip()

        # check if wake word is anywhere at the start (allow some repeated "hey"s)
        if user_input.startswith(WAKE_WORD):
            # Remove wake word
            command = user_input[len(WAKE_WORD):].strip()

            # this will be returned if awakened but nothing is said
            if command == "":
                speak("Yes, sir? Please say a command after 'Hey SAM'.")
                continue
            response = respond_to(command)
            
            if response:
                speak(response)
            
            else:
                # this respoonse will be returned when command not understood
                response = "I'm not sure how to help with that, sir."
                speak(response)

            # goodbye will end program
            if "goodbye" in response.lower():
                break
        else:
            print("Wake word not detected, ignoring input.")
