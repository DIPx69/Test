import telebot
import json
import urllib
import urllib.parse
import requests
import re
import os
import time
import pymongo
import config
import my_module as defx
import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
client = pymongo.MongoClient("mongodb+srv://d6t9:zyYwJLJlnoHK0cwb@dbx.xemx9ia.mongodb.net/?retryWrites=true&w=majority")
bot = telebot.TeleBot("6280451645:AAF5SwVz6S1e-30P7EWZBTTj2Dp8JqHsUHU")
ownerid = 1794942023
@bot.message_handler(commands=['start'])
def send_initial_button(message):
    defx.datack(message)
    return send_home(message)
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
@bot.message_handler(content_types=['text'])
def send_text(message):
   defx.datack(message)
   if message.text == "🔙 Back" or message.text =="❌ Cancel":
       return send_home(message)
   if message.text == '👤 Profile':
      defx.profile(message)
   if message.text == "◼️ Inventory":
      defx.inventory(message)
   if message.text == "💲 Daily":
      defx.daily(message)
   if message.text == "🏪 Shop":
      defx.shopmenu(message)
   if message.text =="🔰 Buy":
      defx.buymenu(message)
   if message.text =="🔰 Buy MineX":
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     minex = datafind['minex']
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Buy ?*\nCurrent Coin: *{coin}*\nCurrent MineX: *{minex}*\nPrice: *{config.minexprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.minexbuymenu)
   if message.text =="🔰 Buy XPBoost":
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     xpboost = datafind['xpboost']
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Buy ?*\nCurrent Coin: *{coin}*\nCurrent XPBoost: *{xpboost}*\nPrice: *{config.xpboostprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.xpboostbuymenu)
   if message.text =="🔰 Sell":
      defx.sellmenu(message)
   if message.text == "🔹 Iron":
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     ammout = datafind['iron']
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Sell ?*\nCurrent Coin: *{coin}*\nCurrent Iron: *{ammout}*\nPrice: *{config.ironprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.ironsell)
   if message.text == "🔹 Coal":
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     ammout = datafind['coal']
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Sell ?*\nCurrent Coin: *{coin}*\nCurrent Coal: *{ammout}*\nPrice: *{config.coalprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.coalsell)
   if message.text == "🔹 Silver":
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     ammout = datafind['silver']
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Sell ?*\nCurrent Coin: *{coin}*\nCurrent Silver: *{ammout}*\nPrice: *{config.silverprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.silversell)
   if message.text == "🔹 Crimsteel":
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     ammout = datafind['crimsteel']
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Sell ?*\nCurrent Coin: *{coin}*\nCurrent Crimsteel: *{ammout}*\nPrice: *{config.crimsteelprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.crimsteelsell)
   if message.text == "🔹 Gold":
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     ammout = datafind['gold']
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Sell ?*\nCurrent Coin: *{coin}*\nCurrent Gold: *{ammout}*\nPrice: *{config.goldprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.goldsell)
   if message.text == "🔹 Mythan":
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     ammout = datafind['mythan']
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Sell ?*\nCurrent Coin: *{coin}*\nCurrent Mythan: *{ammout}*\nPrice: *{config.mythanprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.mythansell)
   if message.text == "🔹 Magic":
     keyboard = telebot.types.ReplyKeyboardMarkup(True)
     keyboard.row('❌ Cancel')
     send = bot.send_message(message.chat.id,"*Fetching Data From Server*",parse_mode="Markdown")
     idx = str(message.chat.id)
     db = client[idx]
     datack = db["data"]
     datafind = datack.find_one()
     coin = datafind["coin"]
     ammout = datafind['magic']
     bot.delete_message(message.chat.id,send.message_id)
     bot.send_message(message.chat.id,f"*How Much You Want To Sell ?*\nCurrent Coin: *{coin}*\nCurrent Magic: *{ammout}*\nPrice: *{config.magicprice}*",parse_mode="Markdown",reply_markup=keyboard)
     bot.register_next_step_handler(message,defx.magicsell)
   if message.text == "up":
      print(1)
      defx.update(message)
   if message.text == '⛏️ Mining':
      defx.miningmenu(message)
   if message.text == "🔷 Iron":
       defx.ironmine(message)
   if message.text == "⛏️ MINE IRON":
      defx.ironminex(message)
print("BOT IS RUNNING..")
bot.polling()
