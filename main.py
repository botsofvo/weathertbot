from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
from test import get_forecasts
from createpage import pagecreator

updater = Updater(token=os.getenv('API_KEY'))

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text = " Hello 🙋  nice to meet you, here are commands 🗒️ you can send me 🔺 and get the reply 🔻 as follows:\n1./location - Send your current location and I will send you 24hr forecast⛅.") 
start_handler= CommandHandler("start",start)

dispatcher.add_handler(start_handler)

# def echo(update, context):
#     context.bot.send_message(chat_id=update.message.chat_id, text="'"+update.message.text+"'\n- by "+update.message.from_user.name)

# echo_handler = MessageHandler(Filters.text, echo)

def get_location(update, context):
    button = [
        [KeyboardButton("Share location", request_location=True)]
        ]
    reply_markup = ReplyKeyboardMarkup(button,"True","True")
    context.bot.send_message(chat_id=update.message.chat_id,
    text="Mind sharing location?",
    reply_markup=reply_markup)

get_location_handler = CommandHandler("location", get_location)

dispatcher.add_handler(get_location_handler)

def location(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    forecasts = get_forecasts(lat, lon)
    data= f'''<br>{forecasts}<br>'''
    pagelink=pagecreator(data)
    button1= [[InlineKeyboardButton(text="click here and read",url=pagelink)]]
    reply_markup1 = InlineKeyboardMarkup(button1)
    context.bot.send_message(chat_id=update.message.chat_id,text="😃 Here is your weather forecast:", reply_markup=reply_markup1,parse_mode='html')
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker="CAACAgQAAxkBAAED8wxiDMYs52Ehx8uqh76tV-JocYlmqwAC5QADZprbKvN4A462THgxIwQ", reply_markup=ReplyKeyboardRemove())
location_handler = MessageHandler(Filters.location, location)
try:
    dispatcher.add_handler(location_handler)
except:
    dispatcher.add_handler(location_handler)
# dispatcher.add_handler(echo_handler)
try:
    updater.start_polling()
except:
    updater.start_polling()
