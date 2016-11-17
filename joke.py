#-*- coding: utf-8 -*-
import telebot
import logging
import json
import os
from telebot import util
import re
from random import randint
import random
import requests as req
import requests
import commands
import urllib2
import urllib
import telebot
import ConfigParser
import redis as r
import redis as redis
from telebot import types
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
token = 'Token' #توکن شما
bot = telebot.TeleBot(token)
redis = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
is_sudo = '192593495' #ایدی شما

print "ربات روشن شد😃"

markupstart = types.InlineKeyboardMarkup()
markupstart.add(types.InlineKeyboardButton('فارسی🇮🇷', callback_data='farsi'))
markupstart.add(types.InlineKeyboardButton('English🇺🇸', callback_data='english'))
markupstartfa = types.InlineKeyboardMarkup()
markupstartfa.add(types.InlineKeyboardButton('😂جک😂', callback_data='getjoke'))
markupstartfa.add(types.InlineKeyboardButton('⭕️ارسال جک به ما⭕️', callback_data='sendjoke'))
markupstartfa.add(types.InlineKeyboardButton('👤توسعه دهنده👤', url='https://telegram.me/ApiCli'), types.InlineKeyboardButton('📢کانال📢', url='https://telegram.me/Special_Programing'))
markupstarten = types.InlineKeyboardMarkup()
markupstarten.add(types.InlineKeyboardButton('😂Joke😂', callback_data='getjokeen'))
markupstarten.add(types.InlineKeyboardButton('⭕️Send us joke⭕️', callback_data='sendjokeen'))
markupstarten.add(types.InlineKeyboardButton('👤Developer👤', url='https://telegram.me/ApiCli'), types.InlineKeyboardButton('📢Channel📢', url='https://telegram.me/Special_Programing'))
markupjoke = types.InlineKeyboardMarkup()
markupjoke.add(types.InlineKeyboardButton('🔘بعدی🔘', callback_data='joke'))
markupjoke.add(types.InlineKeyboardButton('🔙برگشت', callback_data='back'))
markupchuk = types.InlineKeyboardMarkup()
markupchuk.add(types.InlineKeyboardButton('🔘Next🔘', callback_data='chuk'))
markupchuk.add(types.InlineKeyboardButton('🔙Back', callback_data='backen'))
markupavfa = types.InlineKeyboardMarkup()
markupavfa.add(types.InlineKeyboardButton('🔃تغیر زبان🔃', callback_data='avazfa'))
markupaven = types.InlineKeyboardMarkup()
markupaven.add(types.InlineKeyboardButton('🔃Change language🔃', callback_data='avazen'))
markupback = types.InlineKeyboardMarkup()
markupback.add(types.InlineKeyboardButton('🔙برگشت', callback_data='back'))
markupbacken = types.InlineKeyboardMarkup()
markupbacken.add(types.InlineKeyboardButton('🔙Back', callback_data='backen'))

@bot.message_handler(commands=['send'])
def send(message):
        text = message.text.replace('/send ','')
        user = message.from_user.username
        name = message.from_user.first_name
        id = message.chat.id
        bot.send_message(is_sudo, "پیام جدید:\n\nمتن پیام:\n{}\n\nاز طرف:\nیوزرنیم: @{}\nایدی: {}\nاسم: {}".format(text, user, id, name))
        if redis.hget("lang:{}".format(message.chat.id),"farsi"):
            bot.send_message(message.chat.id, "پیام یا انتقاد شما به ما ارسال شد و ما به سروقت به آن رسیدگی میکنیم😊", parse_mode="Markdown")
        elif redis.hget("lang:{}".format(message.chat.id),"english"):
            bot.send_message(message.chat.id, "Your message has been sent and we answer your message soon😊", parse_mode="Markdown")

@bot.message_handler(commands=['toall'])
def toall(m):
    if str(m.from_user.id) == is_sudo:
        text = m.text.replace('/toall','')
        rd = redis.smembers('startmebot')
        for id in rd:
            try:
                bot.send_message(id, "{}".format(text), parse_mode="Markdown")
            except:
                redis.srem('startmebot',id)

@bot.message_handler(commands=['msg'])
def member(m):
    if str(m.from_user.id) == is_sudo:
        id = m.text.split()[1] #ایدی کاربر
        text = m.text.split()[2] #متن
        bot.send_message(id, "{}".format(text), parse_mode="Markdown")

@bot.message_handler(commands=['stats'])
def stats(m):
    if str(m.from_user.id) == is_sudo:
        stats = redis.scard('startmebot')
        bot.send_message(m.chat.id, "`تعداد کاربران`👇\n*{}*".format(stats), parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    id = message.chat.id
    redis.sadd('startmebot',id)
    if redis.hget("lang:{}".format(message.chat.id),"farsi"):
        bot.send_message(message.chat.id, 'زبان فعلی شما فارسی است🇮🇷\nمیتوانید با زدن دکمه ی زیر زبان خود را تغییر دهید🇺🇸', reply_markup=markupavfa)
    elif redis.hget("lang:{}".format(message.chat.id),"english"):
        bot.send_message(message.chat.id, 'Your language now is english🇺🇸\nYou can press down button to set persian language🇮🇷', reply_markup=markupaven)
    else:
        bot.send_message(message.chat.id, "زبان خود را انتخاب کنید👇\nSelect your language👇", reply_markup=markupstart)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "farsi":
          redis.hset("lang:{}".format(call.message.chat.id),"farsi",True)
          redis.hdel("lang:{}".format(call.message.chat.id),"english")
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="زبان شما با موفقیت به فارسی انتخاب شد\n\nلطفا یکدام از دکمه های زیر را انتخاب کنید👇", reply_markup=markupstartfa)
          bot.answer_callback_query(callback_query_id=call.id,text="خوش آمدید😊")
    if call.message:
        if call.data == "english":
          redis.hset("lang:{}".format(call.message.chat.id),"english",True)
          redis.hdel("lang:{}".format(call.message.chat.id),"farsi")
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Your language selected to english🇺🇸\nPlease select one of the button👇", reply_markup=markupstarten)
          bot.answer_callback_query(callback_query_id=call.id,text="Wellcome😊")
    if call.message:
        if call.data == "joke":
          f = open("joke.db")
          text = f.read()
          text1 = text.split(",")
          last = random.choice(text1)
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="{}\n\n[😂ربات جک😂](https://telegram.me/FunJokeBot)".format(last), reply_markup=markupjoke, parse_mode="Markdown")
    if call.message:
        if call.data == "chuk":
          url = "http://tambal.azurewebsites.net/joke/random"
          res = urllib.urlopen(url)
          parsed_json = json.loads(res.read())
          joke = parsed_json['joke']
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="{}\n\n[😂Joke bot😂](https://telegram.me/FunJokeBot)".format(joke), reply_markup=markupchuk, parse_mode="Markdown")
    if call.message:
        if call.data == "avazfa":
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="زبان خود را انتخاب کنید 👇\nSelect your language👇", reply_markup=markupstart)
    if call.message:
        if call.data == "avazen":
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Select your language👇\nزبان خود را انتخاب کنید 👇", reply_markup=markupstart)
    if call.message:
        if call.data == "getjoke":
          f = open("joke.db")
          text = f.read()
          text1 = text.split(",")
          last = random.choice(text1)
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="{}\n\n\n[😂ربات جک😂](https://telegram.me/FunJokeBot)".format(last), reply_markup=markupjoke, parse_mode="Markdown")
    if call.message:
        if call.data == "sendjoke":
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="برای ارسال جک یا انتقاد یا پیشنهاد به ما طبق دستورالعمل زیر عمل کنید👇\n/send متن", reply_markup=markupback)
    if call.message:
        if call.data == "getjokeen":
          url = "http://tambal.azurewebsites.net/joke/random"
          res = urllib.urlopen(url)
          parsed_json = json.loads(res.read())
          joke = parsed_json['joke']
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="{}\n\n\n[😂Joke bot😂](https://telegram.me/FunJokeBot)".format(joke), reply_markup=markupchuk, parse_mode="Markdown")
    if call.message:
        if call.data == "sendjokeen":
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="For send us rate or joke please send👇\n/Send Text", reply_markup=markupbacken)
    if call.message:
        if call.data == "back":
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="به عقب برگشتید🔙\n\nلطفا یکدام از دکمه های زیر را انتخاب کنید👇", reply_markup=markupstartfa)
    if call.message:
        if call.data == "backen":
          bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Come backed🔙\nPlease select one of the button👇", reply_markup=markupstarten)
bot.polling(True)
