import discord
import os
import random
from replit import db
from keep_alive import keep_alive
import urllib.request, json 

from owoify import owoify
import TenGiphPy
# https://github.com/realSnosh/TenGiphPy

from Services import google_search
from Services import quote_search
from Services import roast_database
from Services import to_binary
from Services import isarithmetic
from datetime import datetime


client = discord.Client()

################################################
# Variables
################################################

defaultCommandSymbol = "^"
anime_words = [
    "owo",
    "uwu",
    "x3",
]

starter_roasts = [
  "=w=", ">_>"
  ]

visibleCommands = [
  "inspire (i.e. 'inspire me')", "gif (i.e. 'search a gif for dabbing')", "uwuify (i.e. uwuify to be or not to be)", "youtube" "calculate (i.e. 'calculate the definite integral of x from 0 to 1')",
  "search (i.e. 'search for when discord was made')", "find (i.e. 'find an article about james bond')"
  ]

videoIndicatorWords = [
  "youtube",
  "video"
]

gifIndicators = [
  "gif",
  "gifs"
]

uwuifyIndicators = [
  "uwuify",
  "owoify"
]

helpindicators = [
  "help",
  "assistance",
  "command",
  "cmds"
]

inspireIndicator = [
  "inspire",
  "quote"
]

calculateIndicator = [
  "mathematics",
  "math",
  "calculate",
  "calc",
  "solve",
  "wolfram"
]

calcWhitelistWords = [
  "definite integral",
  "indefinite integral",
  "integrate",
  "derivative",
  "derive",
  "integral",
  "add",
  "subtract",
  "multiply",
  "graph",
  "find max",
  "find min",
  "get max",
  "get min"
]


searchIndicator =[
  "search"
]

findArticle = [
  "article",
  "link",
  "find"
]

slackWords = [
  "in",
  "for",
  "of",
  "to",
  "from",
  "about",
  "search",
  "the",
  "an"
]


def slicer(my_str,sub):
  index=my_str.find(sub)
  if index !=-1 :
    return my_str[(index):] 
  else :
    return my_str

def removeIndicators(string, indicatorArray):
  stri = string.lower()
  for val in indicatorArray:
    stri = slicer(stri, val)

  for val in slackWords:
    try:
      index = stri.find(val)
      if index != -1 and index < (val.length()+1):
        stri = stri[val.length():]
    except:
      continue
  print(stri)
  return stri

def help():
	commandString = ""
	commandString += "**Commands** \n"
	commandString += "You can talk to me about the following \n"
	for val in visibleCommands:
		commandString += "- " + val + "\n"
	return commandString
################################################
# Discord Events
################################################

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.change_presence(activity=discord.Game("DM me"))

@client.event
async def on_message(message):

	if message.author == client.user:
		return

	msg = message.content
	t = TenGiphPy.Tenor(token=os.getenv("TENORKEY"))
	WolframAppId = os.getenv("APPID")

	options = starter_roasts
	if "roasts" in db.keys():
		options += db["roasts"]

  # If bot is mentioned or in dm's
	mention = f'<@!{client.user.id}>'
	if msg.find(mention) == -1:
		mention = f'<@{client.user.id}>'
  
	isDM = isinstance(message.channel, discord.DMChannel)
  
	if mention in msg or isDM:
		try:
			if isDM:
				userText = msg
			else:
				userText = msg.split(mention, 1)[1]
			
			# If Binary, convert to string
			response = ""
			if to_binary.is_Binary(userText):
				response = to_binary.binaryConvert(userText)
			# If not anything, send generic response
			elif any(word in msg.lower() for word in videoIndicatorWords):
				try:
					response = google_search.youtube_search(removeIndicators(userText, videoIndicatorWords))

					voice_state = message.author.voice
					if voice_state is not None:
						author = message.author
						voice_channel = author.voice_channel
						vc = await client.join_voice_channel(voice_channel)

						player = await vc.create_ytdl_player(response)
						player.start()
				except Exception as err:
					print(err)

      # If indicated as gif
			elif any(word in msg.lower() for word in gifIndicators):
				try:
					response = t.random(removeIndicators(userText, gifIndicators))
				except Exception as err:
					print(err)
      # If indicated to find article
			elif any(word in msg.lower() for word in findArticle):
				try:
					links = google_search.get_links(removeIndicators(userText, findArticle), 10)
					response = random.choice(links)
				except Exception as err:
					print(err)

      # If indicated to calculate and do math
			elif any(word in msg.lower() for word in calculateIndicator) or any(word in msg.lower() for word in calcWhitelistWords):
				try:
					textToUse = removeIndicators(userText, calculateIndicator)
					inputVal = textToUse.replace("+", "%2B")
					inputVal = inputVal.replace(" ","+")
					wolfUrl = "https://api.wolframalpha.com/v2/query?input=" + inputVal +"&format=image&output=JSON&appid=" + WolframAppId + "&podstate=Step-by-step%20solution&format=plaintext"
					
					now = datetime.now()

					current_time = now.strftime("%H:%M:%S")
					print(message.author.name, "requested url", wolfUrl, "at", current_time)
					with urllib.request.urlopen(wolfUrl) as url:
						data = json.loads(url.read().decode())
						if data["queryresult"]:

							await message.channel.send("Note that log is the natural log ln, and there may be absolute values not present when calculating the integral.")
							resp1 = data["queryresult"]["pods"][0]["subpods"][0]["img"]["src"]
							print("Response 1", resp1)
							await message.channel.send(resp1)



							response = data["queryresult"]["pods"][1]["subpods"][0]["img"]["src"]

							resp2 = data["queryresult"]["pods"][0]["subpods"][0]["plaintext"]
							print("Response 2", resp2)
							await message.channel.send(resp2)
							await message.channel.send(data["queryresult"]["pods"][0]["subpods"][1]["img"]["src"])

            

				except Exception as err:
					print(err)

      # If indicated to search for information
			elif any(word in msg.lower() for word in searchIndicator):
				try:
					textToUse = removeIndicators(userText, calculateIndicator)
					inputVal = textToUse.replace("+", "%2B")
					inputVal = inputVal.replace(" ","+")
					wolfUrl = "https://api.wolframalpha.com/v2/query?input=" + inputVal +"&format=plaintext&output=JSON&appid=" + WolframAppId
					print(wolfUrl)
					with urllib.request.urlopen(wolfUrl) as url:
						data = json.loads(url.read().decode())
						if data["queryresult"]:
							response = data["queryresult"]["pods"][1]["subpods"][0]["plaintext"]

            

				except Exception as err:
					print(err)
      
      # If indicated to uwuify text
			elif any(word in msg.lower() for word in uwuifyIndicators):
				try:
					response = owoify(removeIndicators(userText, uwuifyIndicators))
				except Exception as err:
					print(err)

      # If indicated to receive help indications
			elif any(word in msg.lower() for word in helpindicators):
				cmd = help()
				await message.author.send(cmd)
        
				if not isDM:
					response = message.author.name + ", check your DM's bro"
				else:
					response = "Hope this helps"

      # If indicated to search for a random quote
			elif any(word in msg.lower() for word in inspireIndicator):
				response = quote_search.get_quote()

      # Else, search Google for a response
			else:
				try:
          # First query type tries to find if Google has
          # a system to find resources
					response = google_search.chatbot_query(userText)
					print(response)
				except:
          # If not, try to find our own resource
					response = google_search.chatbot_query2(userText)
			await message.channel.send(response)

		except:
      # Soon gonna add a small-talk AI bot here, if all else doesn't work
			await message.channel.send(
			    "I'm sorry, it appears that something wrong has occured. Please try again."
			)


keep_alive()
client.run(os.getenv("TOKEN"))
