import telebot
import json
import urllib
import urllib.parse
import requests
import re
import os
import datetime
import time
import config 
import random
import pymongo
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = pymongo.MongoClient("mongodb+srv://d6t9:zyYwJLJlnoHK0cwb@dbx.xemx9ia.mongodb.net/?retryWrites=true&w=majority")
print(client)
bot = telebot.TeleBot("6280451645:AAF5SwVz6S1e-30P7EWZBTTj2Dp8JqHsUHU")
ownerid = 1794942023
def profile(message):
   userx = message.from_user
   username = userx.username
   username = username.replace("_", "\\_")
   idx = str(message.chat.id)
   db = client[idx]
   datack = db["data"]
   datafind = datack.find_one()
   coin = datafind["coin"]
   lvl = datafind["lvl"]
   totalmine = datafind['mymine']
   xp = datafind['xp']
   nxtlvlxp = datafind['nxtlvlxp']
   txt =f"Username: @{username}\n\nTotal Coin : ₪*{coin}*\n\nID : `{idx}`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\nMining Stats|\n━━━━━━━━\nTotal Mining : *{totalmine}*\nLevel : *{lvl}*\nXP BAR : *{xp}/{nxtlvlxp}*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━"
   bot.send_message(message.chat.id,txt,parse_mode="Markdown")
   return send_home(message)
def inventory(message):
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    iron = datafind['iron']
    coal = datafind['coal']
    silver = datafind['silver']
    crimsteel = datafind['crimsteel']
    gold = datafind['gold']
    mythan = datafind['mythan']
    magic = datafind['magic']
    minex = datafind['minex']
    xpboost = datafind['xpboost']
    txt =f"Inventory\n━━━━━━━━━━━━━━━━\nIron: *{iron}*\n━━━━━━\nCoal: *{coal}*\n━━━━━━\nSilver: *{silver}*\n━━━━━━\nCrimsteel: *{crimsteel}*\n━━━━━━\nGold: *{gold}*\n━━━━━━\nMythan: *{mythan}*\n━━━━━━\nMagic: *{magic}*\n━━━━━━━━━━━━━━━━\nItems\n━━━━\nMineX: *{minex}*\nXP Boost: *{xpboost}*\n━━━━━━━━━━━━━━━━"
    bot.send_message(message.chat.id,txt,parse_mode="Markdown")
def send_home(message):
    user = message.chat.id
    user = str(user)
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    if message.chat.id == ownerid:
       keyboard.row('💻 Admin Panel')
    user_id = message.chat.id
    with open('ban.json', 'r') as f:
         ban_ids = json.load(f)
    if any(user_id == ban_id['user_id'] for   ban_id in ban_ids):
      keyboard.row('Account Banned 🚫')
      bot.send_message(message.chat.id, "Account Banned 🚫", parse_mode="Markdown",reply_markup=keyboard)
    else:
       keyboard.row('👤 Profile')
       keyboard.row('💲 Daily','◼️ Inventory','🏪 Shop')
       keyboard.row('⛏️ Mining','⛏️ Auto Mining')
       keyboard.row('◼️ Use Item','◼️ Active Items')
       keyboard.row('⚙️ Settings')
       bot.send_message(message.chat.id, "🏡 Home", parse_mode="Markdown",reply_markup=keyboard)
def ban(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Account Banned 🚫')
    bot.send_message(message.chat.id,"Your Account Is Banned 🚫", parse_mode="Markdown",reply_markup=keyboard)
def dailyx(message):
   idx = str(message.chat.id)
   nxtclaimtimen = int((time.time() + config.dailycooldown))
   db = client[idx]
   collection = db["data"]
   query = {}
   update = {'$inc': {'coin': config.dailycoin}}
   updatetime = {'$set': {'dailycooldown': nxtclaimtimen}}
   collection.update_one(query, updatetime)
   collection.update_one(query, update)
def daily(message):
    timestamp = int(time.time())
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    timestamp2 = datafind['dailycooldown']
    nxttime = datetime.datetime.fromtimestamp(timestamp2).strftime('%d-%m-%Y %I:%M:%S%p')
    user_id = message.chat.id
    with open('ban.json', 'r') as f:
         ban_ids = json.load(f)
    if any(user_id == ban_id['user_id'] for   ban_id in ban_ids):
      bot.send_message(message.chat.id,"You Can't Take Daily Bonus Since Your Account Is Banned.",parse_mode="Markdown")
      return ban(message)
    if timestamp < timestamp2:
       bot.send_message(message.chat.id,f'You Can Claim Again In *{nxttime}*\nIn *{((timestamp - timestamp2)*-1)}* Seconds',parse_mode="Markdown")
    else:
      dailyx(message)
      bot.send_message(message.chat.id,f'You Have Received *{config.dailycoin} Coin*',parse_mode="Markdown")
def datackx(message):
   idx = str(message.chat.id)
   db = client[idx]
   dataadd = db['data']
   dataaddx = {"coin":50,"prestige":0,"minex":0,"minexexp":0,"xpboost":0,"xpboostexp":0,"iron":0,"coal":0,"silver":0,"crimsteel":0,"gold":0,"mythan":0,"magic":0,"mymine":0,"lvl":1,"xp":0,"nxtlvlxp":100,"dailycooldown":0,"minecooldown":0}
   dataadd.insert_one(dataaddx)
def datack(message):
   idx = str(message.chat.id)
   db = client[idx]
   dblist = client.list_database_names()
   if idx not in dblist:
     datackx(message)
def x(message):
   print(10)
   bot.send_message(message.chat.id,"You Can't Take Daily Bonus Since Your Account Is Banned.",parse_mode="Markdown")
def lvlck(message):
    user = message.chat.id
    user = str(user)
    data = json.load(open('user.json', 'r'))
    lvl = data['lvl'][user]
    xp = data['xp'][user]
    nxtlvlxp = data['nxtlvlxp'][user]
    if xp > nxtlvlxp:
       data['lvl'][user] = 2
       data['xp'][user] = 0
       data['nxtlvlxp'][user] += 50
       json.dump(data, open('user.json', 'w'))
       bot.send_message(message.chat.id,f"*You Have Level Up To {(lvl+1)}*",parse_mode="Markdown")
def miningmenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🔷 Iron','🔷 Coal','🔷 Silver')
    keyboard.row('🔷 Crimsteel')
    keyboard.row('🔷 Gold','🔷 Mythan','🔷 Magic')
    keyboard.row('🔙 Back')
    bot.send_message(message.chat.id,"*Select Mining Area*",parse_mode="Markdown",reply_markup=keyboard)
def autominingmenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row("✖️ Auto Mining Feature In Maintenance ✖️")
    keyboard.row('🔙 Back')
    bot.send_message(message.chat.id,"*Select Mining Area*",parse_mode="Markdown",reply_markup=keyboard)
def shopmenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🔰 Buy','🔰 Sell')
    keyboard.row('🔙 Back')
    bot.send_message(message.chat.id,"*Select Item*",parse_mode="Markdown",reply_markup=keyboard)
def sellmenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🔹 Iron','🔹 Coal','🔹 Silver')
    keyboard.row('🔹 Crimsteel')
    keyboard.row('🔹 Gold','🔹 Mythan','🔹 Magic')
    keyboard.row('🔙 Back')
    bot.send_message(message.chat.id,"*Select Item*",parse_mode="Markdown",reply_markup=keyboard)
def ironsell(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    iron = datafind['iron']
    xprice = config.ironprice
    ammout = int(message.text)
    total = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if ammout <= iron:
       bot.send_message(message.chat.id,f"You Have Sold *{message.text}* Iron\n*{total}* Coin Add To Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'iron': -ammout}}
       update1 = {'$inc': {'coin': total}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
           more = ((iron-ammout)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Iron To Sell *{ammout}* Iron",parse_mode="Markdown")
           return sellmenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return sellmenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return sellmenu(message)
  except:
     if message.text == '❌ Cancel':
      return sellmenu(message)
     else:
       bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
       return sellmenu(message)
def coalsell(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    coal = datafind['coal']
    xprice = config.coalprice
    ammout = int(message.text)
    total = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if ammout <= coal:
       bot.send_message(message.chat.id,f"You Have Sold *{message.text}* Coal\n*{total}* Coin Add To Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'coal': -ammout}}
       update1 = {'$inc': {'coin': total}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
           more = ((coal-ammout)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Coal To Sell *{ammout}* Coal",parse_mode="Markdown")
           return sellmenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return sellmenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return sellmenu(message)
  except:
     if message.text == '❌ Cancel':
      return sellmenu(message)
     else:
       bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
       return sellmenu(message)
def silversell(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    name = datafind['silver']
    xprice = config.silverprice
    ammout = int(message.text)
    total = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if ammout <= name:
       bot.send_message(message.chat.id,f"You Have Sold *{message.text}* Silver\n*{total}* Coin Add To Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'silver': -ammout}}
       update1 = {'$inc': {'coin': total}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
           more = ((name-ammout)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Silver To Sell *{ammout}* Silver",parse_mode="Markdown")
           return sellmenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return sellmenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return sellmenu(message)
  except:
     if message.text == '❌ Cancel':
      return sellmenu(message)
     else:
       bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
       return sellmenu(message)
def crimsteelsell(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    name = datafind['crimsteel']
    xprice = config.crimsteelprice
    ammout = int(message.text)
    total = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if ammout <= name:
       bot.send_message(message.chat.id,f"You Have Sold *{message.text}* Crimsteel\n*{total}* Coin Add To Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'crimsteel': -ammout}}
       update1 = {'$inc': {'coin': total}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
           more = ((name-ammout)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Crimsteel To Sell *{ammout}* Crimsteel",parse_mode="Markdown")
           return sellmenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return sellmenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return sellmenu(message)
  except:
     if message.text == '❌ Cancel':
      return sellmenu(message)
     else:
       bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
       return sellmenu(message)
def goldsell(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    name = datafind['gold']
    xprice = config.goldprice
    ammout = int(message.text)
    total = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if ammout <= name:
       bot.send_message(message.chat.id,f"You Have Sold *{message.text}* Gold\n*{total}* Coin Add To Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'gold': -ammout}}
       update1 = {'$inc': {'coin': total}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
           more = ((name-ammout)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Gold To Sell *{ammout}* Gold",parse_mode="Markdown")
           return sellmenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return sellmenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return sellmenu(message)
  except:
     if message.text == '❌ Cancel':
      return sellmenu(message)
     else:
       bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
       return sellmenu(message)
def mythansell(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    name = datafind['mythan']
    xprice = config.mythanprice
    ammout = int(message.text)
    total = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if ammout <= name:
       bot.send_message(message.chat.id,f"You Have Sold *{message.text}* Mythan\n*{total}* Coin Add To Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'mythan': -ammout}}
       update1 = {'$inc': {'coin': total}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
           more = ((name-ammout)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Mythan To Sell *{ammout}* Mythan",parse_mode="Markdown")
           return sellmenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return sellmenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return sellmenu(message)
  except:
     if message.text == '❌ Cancel':
      return sellmenu(message)
     else:
       bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
       return sellmenu(message)
def magicsell(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    name = datafind['magic']
    xprice = config.magicprice
    ammout = int(message.text)
    total = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if ammout <= name:
       bot.send_message(message.chat.id,f"You Have Sold *{message.text}* Magic\n*{total}* Coin Add To Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'magic': -ammout}}
       update1 = {'$inc': {'coin': total}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
           more = ((name-ammout)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Magic To Sell *{ammout}* Magic",parse_mode="Markdown")
           return sellmenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return sellmenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return sellmenu(message)
  except:
     if message.text == '❌ Cancel':
      return sellmenu(message)
     else:
       bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
       return sellmenu(message)
def buymenu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🔰 Buy MineX','🔰 Buy XPBoost')
    keyboard.row('🔙 Back')
    bot.send_message(message.chat.id,"*Select Item*",parse_mode="Markdown",reply_markup=keyboard)
def minexbuymenu(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    xprice = config.minexprice
    ammout = int(message.text)
    totalcost = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if totalcost <= coin:
       bot.send_message(message.chat.id,f"*You Have Purchased *{message.text}* MineX*\n*{totalcost}* Coin Removed From Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'minex': ammout}}
       update1 = {'$inc': {'coin': -totalcost}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
        if len(message.text) <= 10:
           more = ((coin - totalcost)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Coin To Buy *{ammout}* MineX",parse_mode="Markdown")
           return buymenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return buymenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return buymenu(message)
  except:
      if message.text == '❌ Cancel':
       return buymenu(message)
      else:
        bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
        return buymenu(message)
def xpboostbuymenu(message):
  try:
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    coin = datafind["coin"]
    xprice = config.xpboostprice
    ammout = int(message.text)
    totalcost = ammout*xprice
    if message.text == "❌ Cancel":
       return send_home(message)
    if ammout > 0:
      if totalcost <= coin:
       bot.send_message(message.chat.id,f"*You Have Purchased *{message.text}* XPBoost*\n*{totalcost}* Coin Removed From Your Account",parse_mode="Markdown")
       query = {}
       update = {'$inc': {'xpboost': ammout}}
       update1 = {'$inc': {'coin': -totalcost}}
       datack.update_one(query, update)
       datack.update_one(query, update1)
       return send_home(message)
      else:
        if len(message.text) <= 10:
           more = ((coin - totalcost)*-1)
           bot.send_message(message.chat.id,f"You Need More *{more}* Coin To Buy *{ammout}* XPBoost",parse_mode="Markdown")
           return buymenu(message)
    else:
      if ammout == 0:
        bot.send_message(message.chat.id,"* Don't Use 0*",parse_mode="Markdown")
        return buymenu(message)
      else:
        bot.send_message(message.chat.id,"* Don't Use Negetive Number *",parse_mode="Markdown")
        return buymenu(message)
  except:
    if message.text == '❌ Cancel':
       return buymenu(message)
    else:
      bot.send_message(message.chat.id,"*Enter A Valid Number*",parse_mode="Markdown")
      return buymenu(message)
def update(message):
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    query = {}
    update = {"$set": {"new": 25}}
    datack.update_many(query, update)
    bot.send_message(message.chat.id,"Done")
    return send_home(message)
def inventory(message):
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    iron = datafind['iron']
    coal = datafind['coal']
    silver = datafind['silver']
    crimsteel = datafind['crimsteel']
    gold = datafind['gold']
    mythan = datafind['mythan']
    magic = datafind['magic']
    minex = datafind['minex']
    xpboost = datafind['xpboost']
    txt =f"Inventory\n━━━━━━━━━━━━━━━━\nIron: *{iron}*\n━━━━━━\nCoal: *{coal}*\n━━━━━━\nSilver: *{silver}*\n━━━━━━\nCrimsteel: *{crimsteel}*\n━━━━━━\nGold: *{gold}*\n━━━━━━\nMythan: *{mythan}*\n━━━━━━\nMagic: *{magic}*\n━━━━━━━━━━━━━━━━\nItems\n━━━━\nMineX: *{minex}*\nXP Boost: *{xpboost}*\n━━━━━━━━━━━━━━━━"
    bot.send_message(message.chat.id,txt,parse_mode="Markdown")
def ironmine(message):
    txt = "Tap *⛏️ MINE IRON* To Mine"
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('⛏️ MINE IRON')
    keyboard.row('🔙 Back ')
    bot.send_message(message.chat.id,txt,parse_mode="Markdown",reply_markup=keyboard)
def ironminex(message):
    idx = str(message.chat.id)
    db = client[idx]
    datack = db["data"]
    datafind = datack.find_one()
    timestamp = int(time.time())
    maxamm = random.randint(1, config.maxiron)
    maxxp = random.randint(1, config.maxironxp)
    minecooldown = datafind['minecooldown']
    cooldown = config.ironcooldown
    countdownby = config.countdownby
    lvl = datafind['lvl']
    xp = datafind['xp']
    query = {}
    nxtlvlxp = datafind['nxtlvlxp']
    if xp > nxtlvlxp:
       update = {'$inc': {'lvl': +1}}
       update2 = {'$set': {'xp': 1}}
       update3 = {'$inc': {'nxtlvlxp': +50}}
       datack.update_one(query, update)
       datack.update_one(query, update2)
       datack.update_one(query, update3)
       bot.send_message(message.chat.id,f"*You Have Level Up To {(lvl+1)}*",parse_mode="Markdown")
    if timestamp > minecooldown:
       keyboard = telebot.types.ReplyKeyboardMarkup(True)
       keyboard.row(f'Wait {cooldown} Second')
       update2 = {'$inc': {'iron': +maxamm,'xp': +maxxp,'mymine': +1}}
       datack.update_many(query, update2)
       iron = datafind['iron']+maxamm
       txt = f'━━━━━━━━━━━━━━━\nYou Have Mined *{maxamm}* Iron\n━━━━━━━━━━━━━━━\nYou Have Received *{maxxp}* XP\n━━━━━━━━━━━━━━━\nTotal Iron : *{iron}*\n━━━━━━━━━━━━━━━'
       bot.send_message(message.chat.id,txt,parse_mode="Markdown")
       update = {'$set':{'minecooldown': int((timestamp + cooldown/countdownby))}}
       datack.update_one(query, update)
       send = bot.send_message(message.chat.id,f"*{cooldown} Second Left*",parse_mode="Markdown",reply_markup=keyboard)
       print(minecooldown)
       i = cooldown
       while i > 1:
          i -= countdownby
          time.sleep(1)
          keyboard = telebot.types.ReplyKeyboardMarkup(True)
          keyboard.row(f'Wait {i} Second')
          bot.send_message(message.chat.id,f" *{i} Second Left*",parse_mode="Markdown",reply_markup=keyboard)
       return ironmine(message)
    else:
      bot.send_message(message.chat.id,"*Don't Spam Brohhhhhhhh*",parse_mode="Markdown")
def coalmine(message):
    user = message.chat.id
    user = str(user)
    data = json.load(open('user.json', 'r'))
    lvl = data['lvl'][user]
    mincoalvl = config.mincoallvl
    if mincoalvl >= lvl:
       txt = f"You Need More Then *{mincoalvl}* Level To Access This Area"
    else:
       txt = "Tap *⛏️ MINE COAL* To Mine"
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    if mincoalvl >= lvl:
       keyboard.row('Area Restricted 🚫')
       keyboard.row('🔙 Back')
    else:
       keyboard.row('⛏️ MINE COAL')
       keyboard.row('🔙 Back')
    bot.send_message(message.chat.id,txt,parse_mode="Markdown",reply_markup=keyboard)
def coalmine2(message):
    user = message.chat.id
    user = str(user)
    timestamp = int(time.time())
    max = random.randint(1, config.maxcoal)
    maxxp = random.randint(1, config.maxcoalxp)
    data = json.load(open('user.json', 'r'))
    minecooldown = data['minecooldown'][user]
    cooldown = config.coalcooldown
    countdownby = config.countdownby
    lvl = data['lvl'][user]
    xp = data['xp'][user]
    nxtlvlxp = data['nxtlvlxp'][user]
    if xp > nxtlvlxp:
       data['lvl'][user] += 1
       data['xp'][user] = 1
       data['nxtlvlxp'][user] += 50
       json.dump(data, open('user.json', 'w'))
       bot.send_message(message.chat.id,f"*You Have Level Up To {(lvl+1)}*",parse_mode="Markdown")
    if timestamp > minecooldown:
       keyboard = telebot.types.ReplyKeyboardMarkup(True)
       keyboard.row(f'Wait {cooldown} Second')
       data['minecooldown'][user] = int((timestamp + cooldown/countdownby))
       data['coal'][user] += max
       data['xp'][user] += maxxp
       data['mymine'][user] += 1
       ammout = data['coal'][user]
       json.dump(data, open('user.json', 'w'))
       txt = f'━━━━━━━━━━━━━━━\nYou Have Mined *{max}* Coal\n━━━━━━━━━━━━━━━\nYou Have Received *{maxxp}* XP\n━━━━━━━━━━━━━━━\nTotal Coal : *{ammout}*\n━━━━━━━━━━━━━━━'
       bot.send_message(message.chat.id,txt,parse_mode="Markdown")
       send = bot.send_message(message.chat.id,f"*{cooldown} Second Left*",parse_mode="Markdown",reply_markup=keyboard)
       i = cooldown
       while i > 1:
          i -= countdownby
          time.sleep(1)
          keyboard = telebot.types.ReplyKeyboardMarkup(True)
          keyboard.row(f'Wait {i} Second')
          bot.send_message(message.chat.id,f" *{i} Second Left*",parse_mode="Markdown",reply_markup=keyboard)
       return coalmine(message)
    else:
      bot.send_message(message.chat.id,"*Don't Spam Brohhhhhhhh*",parse_mode="Markdown")