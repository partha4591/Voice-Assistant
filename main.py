# Here are the list of modules that are required for this project
from bs4 import BeautifulSoup
import pyttsx3                           #For audio
import speech_recognition as sr          # To recognize the audio from the user
from datetime import datetime
import webbrowser as wb
import json                              # To receive json files
from jsonpath import jsonpath            # To extract information from json
import requests                          # To send and receive API requests
import pywhatkit as kit                  # Module for automation
import wikipedia as wiki

# https://api.genderize.io?name=   To get API request of the names

global text

engine = pyttsx3.init("sapi5")                     # Initialise the sapi5 microsoft speech API
voice = engine.getProperty("voices")               # Initialising voice property  
engine.setProperty("voice", voice[3].id)           # Setting the voice audio which we want to hear
engine.setProperty("rate", 230)                    # Setting the speed limit of the speech

recognizer = sr.Recognizer()                       # Initializing recognizer class
mic = sr.Microphone()                              # Setting the mic


# Creating function to speak

def Say(command):
    engine.say(command)
    engine.runAndWait()

# Asking the user to enter their name

def askfull_name():
    global name
    global user_name
    Say("Hi. May I know your name??")
    full_name = input("Enter your name: ")
    name = tuple(full_name.split(" "))
    user_name = name[0]

# This function will determine the gender based on their names

def determineGender(NAME):
    url = f"https://api.genderize.io?name={NAME}"
    response = requests.get(url)                         # Getting request url from the api

    json_response = json.loads(response.text)            # Getting the json file in the form of text
    gender_response = jsonpath(json_response, "gender")  # Specifying only particular property of the json file

    gender = gender_response[0]

    if gender == "male":
        return "sir"

    else:
        return "ma'am"


# wishMe function to greet the user based on which time the user is entering

def wishMe():
    global hour
    global currentDate
    currentDate = datetime.now()
    hour = currentDate.hour

    if hour > 12 and hour <= 15:
        Say(f"Good afternoon {user_name}{determineGender(user_name)}")

    elif hour >= 5 and hour < 12:
        Say(f"Good morning {user_name}{determineGender(user_name)}")

    elif hour > 15 and hour < 20:
        Say(f"Good evening {user_name}{determineGender(user_name)}")

    elif hour == 12:
        Say(f"Good noon {user_name}{determineGender(user_name)}")

    else:
        Say(f"Nice to meet you {user_name}{determineGender(user_name)}")


# Function to tell the time to user

def TellTime():
    currentTime = currentDate.strftime("%I:%M %p")  # Setting the time format in the string which you will be able to find in the website https://www.w3schools.com/python/python_datetime.asp

    time = f"Time is now {currentTime}"
    print(time)
    engine.say(time)
    engine.say("Anything more sir??")
    engine.runAndWait()

# searchOnYoutube function to search something or play videos on youtube as per user request

def searchOnYoutube():
    # Below is the logic to find the exact thing the user want to search

    new_list = list(text.split(" "))               # Breaking the string into list
    searched_content = []                          # New list to find the searched content
    for i in range(1, len(new_list)):              # 1 is taken as the starting range because user will obviously say "search ...." or "play ...". For that it is ignored

        if new_list[i] == "on" and new_list[i + 1] == "youtube":
            break

        else:
            searched_content.append(new_list[i])

    # After finding the searched content into the new list to string

    searching_element = " ".join(searched_content)

    if "play" in text:
        kit.playonyt(searching_element)
    else:
        wb.open(f"https://www.youtube.com/results?search_query={searching_element}")


# Tell_Day function to tell about current day 
def Tell_Day():
    day = currentDate.day
    today = currentDate.strftime("%A")
    monthname = currentDate.strftime("%B")
    wHoleday = f"Today is {today} {day} {monthname} {currentDate.year}"
    print(wHoleday)
    engine.say(wHoleday)
    engine.say(f"Anything do you want to know {determineGender(user_name)} ?")
    engine.runAndWait()


#googleSearch funtion to... obviously google search
def googleSearch(search_item):
    url = "https://google.com/search?q=" + search_item
    request_result = requests.get(url)

    #BeautifulSoup is the module to parse html content
    soup = BeautifulSoup(request_result.content, "html.parser")

    # "BNeawe iBp4i AP7Wnd" is the class name in the division in which the answer or search result is written and it is used to find only that section

    try:
        result = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
        print(result)
        engine.say(result)
        engine.runAndWait()

    # And if it fails to find that class, it will directly show the user search result

    except AttributeError:
        Say("Here is the result")
        kit.search(search_item)


# Function to perform wikipedia search and also speak the result
def search_on_Wikipedia(search_content):
    result = wiki.summary(search_content, 1)   # wiki.summary(search_content, 1) this parameter takes the topic(string) and no: of lines/sentences it will give which is set to 1
    print(result)
    Say(result)


if __name__ == "__main__":
    askfull_name()
    wishMe()
    Say("How may i help you??")
    while True:
        try:
            with mic as source:                                  # Adjusting mic as source
                recognizer.adjust_for_ambient_noise(source)      # Adjusts the energy threshold with the ambient energy level
                print("Listening...")
                audio = recognizer.listen(source)                # To listen audio from the user
                recognizer.pause_threshold = 1                   # Setting the pause_threshold to 1 sec,i.e, minimum seconds of speaking audio before we consider the speaking audio to be finished

                text = recognizer.recognize_google(audio, language="en-in")     # To recognize the audio using google speech recognition mode 
                text = str(text).lower()                                        # Converting the speech to lowercase letters because sometimes it will produce some uppercase letters

                # Here are the list of commands that user might speak and taking actions according to that

                if "stop" in text or "no thanks" in text or "leave it" in text:
                    print(text)
                    if hour >= 20 or hour < 5:
                        Say(f"Good night {determineGender(user_name)}. Have a nice day")
                        engine.stop()
                        break

                    else:
                        Say(f"Good bye {determineGender(user_name)}. Have a nice day")
                        engine.stop()
                        break

                elif text == "how are you":
                    Say("I am fine")

                elif "open youtube" in text:
                    print("opening Youtube")
                    Say("Opening youtube")
                    wb.open("https://www.youtube.com/")
                    break

                elif "on youtube" in text or "in youtube" in text or "play" in text:
                    print(text)
                    searchOnYoutube()
                    break

                elif "time" in text:
                    TellTime()

                elif "facebook" in text:
                    fb = "Opening FaceBook"
                    print(fb)
                    engine.say(fb)
                    engine.runAndWait()
                    wb.open("https://www.facebook.com/")
                    break

                elif "my name" in text:
                    namestatement = f"Your name is {name}"
                    print(namestatement)
                    Say(namestatement)

                elif "today" in text:
                    Tell_Day()

                elif "who is" in text or "who are" in text or "what is" in text or "what are" in text:
                    search_on_Wikipedia(text)
                    Say(
                        f"Do you want to know anything else {determineGender(user_name)} ?"
                    )

                elif "who are you" in text:
                    Say("You know, I am something of Jarvis, Friday, Siri etc myself")
                    
                else:
                    print(text)
                    googleSearch(text)
                    Say(f"Anything more {determineGender(user_name)}?")
        # In case if it's failed to recognize audio then it will speak this
        except:
            Say(f"Sorry...could not fetch your speech {user_name}. Try again")

