import discord
import os
import random
from replit import db
from keep_alive import keep_alive

from owoify import owoify
import TenGiphPy
# https://github.com/realSnosh/TenGiphPy

from Services import google_search
from Services import quote_search
from Services import roast_database
from Services import to_binary

client = discord.Client()
t = TenGiphPy.Tenor(token=os.getenv("TENORKEY"))

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
  "inspire", "gif [text]", "uwuify [text]", "youtube [text]"
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

slackWords = [
  "in",
  "for",
  "of",
  "to",
  "from",
  "about",
  "search"
]

def slicer(my_str,sub):
  index=my_str.find(sub)
  if index !=-1 :
    return my_str[index:] 
  else :
    return my_str

def removeIndicators(string, indicatorArray):
  stri = string.lower()
  for val in indicatorArray:
    stri = slicer(stri, val)
    stri = stri.replace(val, '')

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
	commandString += "Note: You can talk to me to find stuff \n"
	for val in visibleCommands:
		commandString += "- " + val + "\n"
	return commandString
################################################
# Discord Events
################################################

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.change_presence(activity=discord.Game("Talk to me"))

@client.event
async def on_message(message):

	if message.author == client.user:
		return

	msg = message.content

	options = starter_roasts
	if "roasts" in db.keys():
		options += db["roasts"]

  # If bot is mentioned or in dm's
	mention = f'<@!{client.user.id}>'
	if msg.find(mention) == -1:
		mention = f'<@{client.user.id}>'
  
	isDM = isinstance(message.channel, discord.DMChannel) and msg.find(mention) == -1
  
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
				except:
					print()
			elif any(word in msg.lower() for word in gifIndicators):
				try:
					response = t.random(removeIndicators(userText, gifIndicators))
				except:
					print()
			elif any(word in msg.lower() for word in uwuifyIndicators):
				try:
					response = owoify(removeIndicators(userText, uwuifyIndicators))
				except:
					print()
			elif any(word in msg.lower() for word in helpindicators):
				cmd = help()
				await message.author.send(cmd)
				response = message.author.name + ", check your DM's bro"
			elif any(word in msg.lower() for word in inspireIndicator):
				response = quote_search.get_quote()
			else:
				try:
					response = google_search.chatbot_query(userText)
					print(response)
				except:
					response = google_search.chatbot_query2(userText)
          # if response == "":
          #  response = str(english_bot.get_response(query))
			await message.channel.send(response)

		except:
			await message.channel.send(
			    "I'm sorry, it appears that something wrong has occured. Please try again."
			)


keep_alive()
client.run(os.getenv("TOKEN"))
