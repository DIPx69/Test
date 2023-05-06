import sklearn
import telebot
import pymongo

import dns.resolver

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)

dns.resolver.default_resolver.nameservers=['8.8.8.8']

ownerid = 1794942023

client = pymongo.MongoClient("mongodb+srv://d6t9:zyYwJLJlnoHK0cwb@dbx.xemx9ia.mongodb.net/?retryWrites=true&w=majority",serverSelectionTimeoutMS=5000)

bot = telebot.TeleBot("6280451645:AAF5SwVz6S1e-30P7EWZBTTj2Dp8JqHsUHU")

#bot.send_message(ownerid,client)

def datack(message):

   idx = str(message.chat.id)

   db = client[idx]

   coinadd = db['coin']

   lvladd = db['lvl']

   send = bot.send_message(message.chat.id,"*Creating Database For You*",parse_mode="Markdown")

   bot.edit_message_text("*Adding Coin*", message.chat.id, send.message_id,parse_mode="MarkdownV2")

   coinaddx = {"coin": 50}

   coinadd.insert_one(coinaddx)

   bot.edit_message_text("*Adding Level*", message.chat.id, send.message_id,parse_mode="MarkdownV2")

   lvladdx = {"lvl": 1}

   lvladd.insert_one(lvladdx)

   return send_home(message)

def send_home(message):

    bot.send_message(message.chat.id, "🏡 Home", parse_mode="Markdown")

@bot.message_handler(commands=['start'])

def send_start(message):

   idx = str(message.chat.id)

   db = client[idx]

   dblist = client.list_database_names()

   if idx not in dblist:

     datack(message)

   return send_home(message)

@bot.message_handler(commands=['test'])

def send_test(message):

   idx = str(message.chat.id)

   db = client[idx]

   collectionlist = db.list_collection_names()

   print(collectionlist)

   if "coin" not in collectionlist:

     print(1)

   else:

     print(2)

@bot.message_handler(commands=['xtz'])

def send_xtz(message):

   idx = str(message.chat.id)

   db = client[idx]

   dblist = client.list_database_names()

   print(dblist)

   if idx in dblist:

     bot.send_message(message.chat.id,idx)

   else:

     bot.send_message(message.chat.id,"Sad")

@bot.message_handler(commands=['daily'])

def send_daily(message):

   idx = str(message.chat.id)

   db = client[idx]

   collection = db["coin"]

   query = {}

   update = {'$inc': {'coin': 1}}

   collection.update_one(query, update)

   bot.send_message(message.chat.id,"Add")

@bot.message_handler(commands=['profile'])

def send_profile(message):

   idx = str(message.chat.id)

   db = client[idx]

   coinck = db["coin"]

   lvlck = db["lvl"]

   coinckx = coinck.find()

   lvlckx = lvlck.find()

   for coin in coinckx:

    coin = coin["coin"]

   for lvl in lvlckx:

    lvl = lvl["lvl"]

   bot.send_message(message.chat.id,f"Coin : {coin}\nLevel: {lvl}")

   return send_home(message)

print("Bot Is Running") 

bot.polling()

