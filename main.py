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


################################################
# Variables
################################################

defaultCommandSymbol = "$"
anime_words = [
    "owo",
    "uwu",
    "x3",
]

starter_roasts = [
  "=w=", ">_>"
  ]

visibleCommands = [
  "inspire", "gif [text]", "uwuify [text]", "chika"
  ]


################################################
# Discord Events
################################################

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  if "symbol" in db.keys():
    print("test")
  else:
  	db["symbol"] = defaultCommandSymbol
  await client.change_presence(activity=discord.Game(db["symbol"] + "help"))

@client.event
async def on_message(message):
	symbol = db["symbol"]

	if message.author == client.user:
		return

	msg = message.content

	options = starter_roasts
	if "roasts" in db.keys():
		options += db["roasts"]

	# help
	if msg.startswith(symbol + "help"):
		commandString = ""
		commandString += "**Commands** \n"
		for val in visibleCommands:
			commandString += symbol + val + "\n"
		await message.author.send(commandString)
		await message.channel.send(message.author.name +
		                           ", check your DM's bro")

	# inspire
	if msg.startswith(symbol + "inspire"):
		quote = quote_search.get_quote()
		await message.channel.send(quote)

	# anime words
	if any(word in msg.lower() for word in anime_words):
		await message.channel.send(random.choice(options))

	# add roast
	if msg.startswith(symbol + "addroast"):
		roastmessage = msg.split(symbol + "addroast ", 1)[1]
		roast_database.update_roasts(roastmessage)
		await message.channel.send(
		    message.author.name +
		    ", your roast has been added to the database.")

	# say something
	if msg.startswith(symbol + "say"):
		userText = msg.split(symbol + "say ", 1)[1]
		await message.channel.send(userText)
		await message.delete()

	# search for a gif
	if msg.startswith(symbol + "gif"):
		userText = msg.split(symbol + "gif ", 1)[1]
		try:
			t = TenGiphPy.Tenor(token=os.getenv("TENORKEY"))
			await message.channel.send(t.random(userText))
		except:
			await message.channel.send(
			    "Could you please be more elaborate with your response?")

	# uwuify
	if msg.startswith(symbol + "uwuify"):
		userText = owoify(msg.split(symbol + "uwuify ", 1)[1])
		await message.channel.send(userText)

	# monke
	if "monke" in message.content:
		await message.channel.send("https://youtu.be/M69Sn3OERZo")

	# delete roast
	if msg.startswith(symbol + "delroast"):
		roasts = []
		if "roasts" in db.keys():
			index = int(msg.split(symbol + "delroast", 1)[1])
			roast_database.delete_roast(index)
			roasts = db["roasts"]

		await message.channel.send(
		    message.author.name +
		    ", your roast has been removed at index. : " + str(roasts))

	# list roasts
	if msg.startswith(symbol + "listroasts"):
		roasts = db["roasts"]
		await message.channel.send(roasts)

	# change symbol
	if msg.startswith(symbol + "changesymbol"):
		newSymbol = msg.split(symbol + "changesymbol ", 1)[1]
		db["symbol"] = newSymbol
		await message.channel.send(message.author.name +
		                           ", symbol changed to " + newSymbol)
		await client.change_presence(activity=discord.Game(db["symbol"] +
		                                                   "help"))

	# chika
	if "chika" in message.content:
		await message.channel.send(
		    "https://media.tenor.com/images/fe3826b59f80f5e6c7cc04eb474fb44d/tenor.gif"
		)


  # If bot is mentioned
	mention = f'<@!{client.user.id}>'
	if mention in msg:
		try:
			userText = msg.split(mention, 1)[1]
			# If Binary, convert to string
			response = ""
			if to_binary.is_Binary(userText):
				response = to_binary.binaryConvert(userText)
			# If not anything, send generic response
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
