
import os
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import wolframalpha
import webbrowser
from urllib.request import urlopen
import json
import requests
import pywhatkit
import subprocess
import pyjokes
import time

assistantname = 'nimaary'
user_name = ""
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

# The pyttsx3 module is stored in a variable name engine.
# Sapi5 is a Microsoft Text to speech engine used for voice recognition.
# The voice Id can be set as either 0 or 1,
# 0 indicates Male voice
# 1 indicates Female voice

# The init function is the main function, 
# we have to use this function every time. 
# This function initializes the connection and creates an engine 
# and we can perform all the things on the engine created by the .init() function
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Converts text to speech
def speak(text):
	engine.say(text)
	# This function Blocks while processing all currently queued commands. 
	# It Invokes callbacks for engine notifications appropriately 
	# and returns back when all commands queued before this call are emptied from the queue.
	engine.runAndWait()

# Wishes the user
def wishMe():
	hour = datetime.datetime.now().hour

	if hour>=0 and hour<12:
		speak("Hello, Good Morning")
		print("Hello, Good Morning")
	elif hour>=12 and hour<18:
		speak("Hello, Good Afternoon")
		print("Hello, Good Afternoon")
	else:
		speak("Hello, Good Evening")
		print("Hello, Good Evening")

	speak("I am your Assistant " + assistantname)

def username():
	speak("What should I call you?")
	user_name = takeCommand()
	speak("Welcome "+ user_name)
     
	print("#####################")
	print("Welcome, ", user_name)
	print("#####################")
     
	speak("How can I help you?")

# Takes commands from the user and returns the statement
def takeCommand():
	r = sr.Recognizer()

	with sr.Microphone() as source:
		print("Listening....")
		r.pause_threshold = 1

		r.adjust_for_ambient_noise(source, duration = 0.2)
		audio = r.listen(source)

		try:
			statement = r.recognize_google(audio, language='en-in')
			print(f"user said:{statement}\n")

		except Exception as e:
			return "None"

		return statement


if __name__ == '__main__':
	clear = lambda: os.system('cls')
     
    # This Function will clean any
    # command before execution of this python file
	clear()
	wishMe()
	username()


	while True:

		statement = takeCommand().lower()

		print(statement)

		if statement is None or "none" in statement:
			continue

		elif 'bye' in statement or 'stop' in statement or 'quit' in statement:
			speak("Have a good day, "+ user_name)
			speak("Bye")
			print("Bye")
			break

		# Fetching information from wikipedia
		elif 'wikipedia'in statement or 'what is'in statement:
			statement = statement.replace("wikipedia", "")
			statement = statement.replace("what is", "")
			print(statement)

			results = wikipedia.summary(statement, sentences = 2)  
			speak("According to Wikipedia: ")
			print(results)
			speak(results)
			speak("Thank you!")
			speak("Is there something else for me?")

		# Opening a browser tab
		elif 'open youtube' in statement:
			speak("Opening youtube")
			print("Opening youtube")
			webbrowser.get(chrome_path).open_new_tab("https://www.youtube.com")
			time.sleep(5)

		elif 'open google' in statement or 'open chrome' in statement:
			speak("Opening google")
			print("Opening google")
			webbrowser.get(chrome_path).open_new_tab("https://www.google.com")
			time.sleep(5)

		elif 'open gmail' in statement:
			speak("Opening gmail")
			print("Opening gmail")
			webbrowser.get(chrome_path).open_new_tab("https://www.gmail.com")
			time.sleep(5)

		# Getting current time
		elif 'time' in statement:
			strTime = datetime.datetime.now().strftime("%I:%M %p")
			speak(f"The time is {strTime}")
			print(f"The time is {strTime}")
			speak("Is there something else for me?")

		
		elif 'news' in statement:
             
			try:
				jsonObj = urlopen('https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=d5a2c4fd761c4ffcab96c3b24ee7660b')
				data = json.load(jsonObj)
				i = 1

				speak('here are some top news from the times of india')
				print('''=============== TIMES OF INDIA ============'''+ '\n')

				for i in range(3):

					print(str(i) + '. ' + data['articles'][i]['title'] + '\n')
					print(data['articles'][i]['description'] + '\n')
					speak(str(i) + '. ' + data['articles'][i]['title'] + '\n')
					i += 1

			except Exception as e:
				print(str(e))

			speak("Thank you!")
			speak("Is there something else for me?")


		# Searching data from web
		elif 'search' in statement:
			statement = statement.replace("search", "")
			webbrowser.get(chrome_path).open_new_tab("https://www.google.com/search?q="+statement)
			time.sleep(5)

		# Weather forecast
		elif "weather" in statement or "climate" in statement:
             
            # Using Open weather API
			speak("City name?")
			
			city_name = takeCommand()
			print("City name : ", city_name)

			complete_url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&units=metric&appid=16887a09cc73abe7c6e21b9d50d17bfa'
			response = requests.get(complete_url)
			x = response.json()
             
			if x["cod"] != "404":
				y = x["main"]
				current_temperature = y["temp"]
				current_pressure = y["pressure"]
				current_humidiy = y["humidity"]
				z = x["weather"]
				weather_description = z[0]["description"]
				speak(" \nTemperature " +str(current_temperature) + " Kelvin"+"\n atmospheric pressure "+str(current_pressure) + "hPa" +"\n humidity " +str(current_humidiy) + "percentage" +"\n description " +str(weather_description))
				print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))
             
			else:
				speak(" City Not Found ")


			speak("Thank you!")
			speak("Is there something else for me?")

		# Playing song using pywhatkit
		elif 'song' in statement or 'play song' in statement or 'music' in statement:
			song = statement.replace('play', '')
			speak("Playing " + song)
			pywhatkit.playonyt(song)
			time.sleep(5)

		# To log off the PC:
		elif "log off" in statement or "shutdown" in statement:
			speak("Okay, your pc will log off in 10 seconds. Make sure you exit from all the applications")
			subprocess.call(["shutdown", "/l"])
			time.sleep(3)

		# A joke
		elif 'joke' in statement:
			speak("Get ready for a joke!")
			joke = pyjokes.get_joke()
			print(joke)
			speak(joke)
			speak("Hah hah! Wasn't that funny?")
			speak("Is there something else for me?")

		elif "calculate" in statement:

			app_id = "QUJGXK-KWK2XT5J5A"
			client = wolframalpha.Client(app_id)
			indx = statement.lower().split().index('calculate')
			statement = statement.split()[indx + 1:]
			res = client.query(' '.join(statement))
			answer = next(res.results).text
			print("The answer is " + answer)
			speak("The answer is " + answer)

			speak("Is there something else for me?")

		# Tells location
		elif "where is" in statement or "location of" in statement:
			statement = statement.replace("where is", "")
			statement = statement.replace("location of", "")
			location = statement
			speak("Locating"+location)
			webbrowser.get(chrome_path).open_new_tab("https://www.google.com/maps/place/"+statement)
			time.sleep(3)

		# -----------------------------------------

		elif assistantname in statement or "nimari" in statement:
			wishMe()
			speak(assistantname+" in your service!")

		elif 'who are you' in statement or 'what can you do' in statement:
			speak("I am "+assistantname+", your virtual assistant. I can help you with certain tasks. Tell me, what's in your mind "+ user_name +"?")

		elif 'your name' in statement or 'name' in statement:
			speak("My friends call me " + assistantname +". Well, you can call me anything " + user_name + ".")

		elif 'how are you' in statement:
			speak("I am fine, Thank you!")
			speak("How are you? , " + user_name)
 
		elif 'fine' in statement or "good" in statement or "great" in statement:
			speak("It's good to know that")

		elif 'you are very' in statement or "you are awesome" in statement or "you are cute" in statement or "you are smart" in statement:
			speak("So sweet of you! Thank you")

		elif "hello" in statement or "hi" in statement or "morning" in statement or "evening" in statement:
			wishMe()

		else:
			speak("Pardon me! I did not get you.")






		

