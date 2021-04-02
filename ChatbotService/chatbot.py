from chatterbot import ChatBot
# Create object of ChatBot class

# Inport ListTrainer
from chatterbot.trainers import ListTrainer

bot = ChatBot(
    'Buddy',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)

trainer = ListTrainer(bot)

trainer.train([
'Hi',
'Hello',
'I need your assistance regarding my order',
'Please, Provide me with your order id',
'I have a complaint.',
'Please elaborate, your concern',
'How long it will take to receive an order ?',
'An order takes 3-5 Business days to get delivered.',
'Okay Thanks',
'No Problem! Have a Good Day!'
])