import discord
import os
import random
from keep_alive import keep_alive
import urllib.request, json
import time

from owoify import owoify
import TenGiphPy
# https://github.com/realSnosh/TenGiphPy

from Services import google_search
from Services import quote_search
from Services import to_binary
from datetime import datetime
from Services import eight_ball
from youtube_dl import YoutubeDL
from discord.utils import get
from discord import FFmpegPCMAudio

# Retrieve keys from .env storage 
# (Note, you can replace os.getenv("tokenname") with "key")
discordKey = os.getenv("TOKEN")
# Discord Key is from https://discord.com/developers/applications
# Create bot, then go to Bot -> Token -> Copy
tenorBotKey = os.getenv("TENORKEY")
# Retrieved from https://tenor.com/developer/keyregistration
WolframAppId = os.getenv("APPID")
# Key retrieved from https://products.wolframalpha.com/simple-api/documentation/


tenorBot = TenGiphPy.Tenor(token=tenorBotKey)
client = discord.Client()


################################################
# Variables
################################################

# List of commands
visibleCommands = [
  "inspire (i.e. 'inspire me')", "gif (i.e. 'search a gif for dabbing')", "uwuify (i.e. uwuify to be or not to be)", "youtube" "calculate (i.e. 'calculate the definite integral of x from 0 to 1')",
  "search (i.e. 'search for when discord was made')", "find (i.e. 'find an article about james bond')", "image (i.e. 'find an image of James Bond')", "play (i.e. 'play Astronaut in the Ocean'"
]

# Indication of words to search for a youtube video
videoIndicatorWords = [
  "youtube",
  "video"
]

# Indication to search for a gif
gifIndicators = [
  "gif",
  "gifs"
]

# Indication of words to get uwu stuff
uwuifyIndicators = [
  "uwuify",
  "owoify"
]

# Indication words to receive commands
helpindicators = [
  "help",
  "assistance",
  "command",
  "cmds"
]

# Indication words to receive a quote
inspireIndicator = [
  "inspire",
  "quote"
]

# Indication words to calculate or do math
calculateIndicator = [
  "mathematics",
  "math",
  "calculate",
  "calc",
  "solve",
  "wolfram"
]

# Indication words to calculate or do math, but will be kept in the message
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
  "plot",
  "find max",
  "find min",
  "get max",
  "get min"
]

# Indication words to search for information 
searchIndicator =[
  "search"
]

# Indication words to play for music 
playIndicator =[
  "play"
]

# Indication words for disconnecting from voice channel
discionnectIndicators = [
  "disconnect",
  "dc",
  "leave",
  "bye"
]

# Indication words to find an article on the internet and share a link
findArticle = [
  "article",
  "link",
  "find"
]

# Indication of image search
findImage = [
  "picture",
  "image",
  "illustration",
  "illustrate",
  "img",
  "pic"
]

# Words that should be removed if they are in front of the indication that is found
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

  # If bot is mentioned or in dm's
	mention = f'<@!{client.user.id}>'
	if msg.find(mention) == -1:
		mention = f'<@{client.user.id}>'
  
	isDM = isinstance(message.channel, discord.DMChannel)
	channel_nsfw = False
	if not isDM:
		channel_nsfw = message.channel.is_nsfw()
  
	if mention in msg or isDM:
		try:
			if isDM:
				userText = msg
			else:
				userText = msg.split(mention, 1)[1]
			
			

			response = ""

			# If another user is mentioned, we would do an 8 ball response
			if len(message.mentions) > 1:
				# print("test")
				try:
					mes = userText.lower()
					if mes.find("what") != -1 or mes.find("where") != -1:
						response = eight_ball.what_ball()
					elif mes.find("who") != -1:
						response = eight_ball.who_ball()
					elif mes.find("why") != -1:
						response = eight_ball.why_ball()
					else:
						response = eight_ball.eight_ball()
				except Exception as err:
					print(err)

			# If Binary, convert to string
			elif to_binary.is_Binary(userText):
				response = to_binary.binaryConvert(userText)

      # If indicated to find an image
			elif any(word in msg.lower() for word in findImage):
				if channel_nsfw:
					try:
						random.seed(time.time())
						response = google_search.image_search(removeIndicators(userText, findImage), False)

					except Exception as err:
						if str(err).find("429") != -1:
							message.channel.send("Img quota exceeded, scraping...")
							response = google_search.image_search2(removeIndicators(userText, findImage), False)
						else:
							response = "Something with image search went wrong."

						print(err)
				else:
					try:
						random.seed(time.time())
						response = google_search.image_search(removeIndicators(userText, findImage), True)
						print(response)

					except Exception as err:
						if str(err).find("429") != -1:
							message.channel.send("Img quota exceeded, scraping...")
							response = google_search.image_search2(removeIndicators(userText, findImage), True)
						else:
							response = "Something with image search went wrong."
						print(err)

      # Disconnect from voice channel
			elif any(word in msg.lower() for word in discionnectIndicators):
				try:
					for x in client.voice_clients:
						if(x.guild == message.guild):
							return await x.disconnect()
					response = "Done :+1:"
				except:
					response = "Something went wrong..."

			# If video/youtube key word, search for a YouTube video or play a youtube song
			elif any(word in msg.lower() for word in videoIndicatorWords) or any(word in msg.lower() for word in playIndicator):
				try:

					toPlayMusic = any(word in msg.lower() for word in playIndicator)
					response = google_search.youtube_search(removeIndicators(removeIndicators(userText, videoIndicatorWords), playIndicator))

					if toPlayMusic:
						await message.channel.send("Loading Song")
						YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
						FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
						voice = get(client.voice_clients, guild=message.guild )
						voice_channel = message.author.voice.channel

						if not voice or not voice.is_playing() or voice != voice_channel:
							if voice != voice_channel:
								voice = await voice_channel.connect()

							with YoutubeDL(YDL_OPTIONS) as ydl:
								info = ydl.extract_info(response, download=False)
							URL = info['formats'][0]['url']
							voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
							voice.is_playing()
							await message.channel.send("Playing")
						else:
							await message.channel.send("Already playing song")
							return
            
				except Exception as err:
					print(err)

      # If indicated as gif
			elif any(word in msg.lower() for word in gifIndicators):
				try:
					random.seed(time.time())
					response = tenorBot.random(removeIndicators(userText, gifIndicators))
				except Exception as err:
					print(err)
      # If indicated to find article
			elif any(word in msg.lower() for word in findArticle):
				try:
					random.seed(time.time())
					links = google_search.get_links(removeIndicators(userText, findArticle))
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
client.run(discordKey)