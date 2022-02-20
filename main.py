from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
from test import get_forecasts
from createpage import pagecreator
import time
# from dotenv import load_dotenv

# load_dotenv()

updater = Updater(token=os.getenv('API_KEY'))

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text = " Hello 🙋  nice to meet you, here are commands 🗒️ you can send me 🔺 and get the reply 🔻 as follows:\n1./location - Send your current location and I will send you 24hr forecast⛅.") 

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="'"+update.message.text+"'\n- by "+update.message.from_user.name)

def get_location(update, context):
    button = [
        [KeyboardButton("Share location", request_location=True)]
        ]
    reply_markup = ReplyKeyboardMarkup(button,"True","True")
    context.bot.send_message(chat_id=update.message.chat_id,
    text="Mind sharing location?",
    reply_markup=reply_markup)

def location(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    forecasts = get_forecasts(lat, lon)
    data= f'''{forecasts}'''
    pagepath=pagecreator(data)
    pagelink=f'https://telegra.ph/{pagepath}'
    button1= [[InlineKeyboardButton(text="click here and read",url=pagelink)]]
    reply_markup1 = InlineKeyboardMarkup(button1)
    context.bot.send_message(chat_id=update.message.chat_id,text="loading..... pls wait", reply_markup=reply_markup1)
    while True:
        try:
            context.bot.send_message(chat_id=update.message.chat_id,text="😃 Here is your weather forecast:", reply_markup=reply_markup1)
            context.bot.send_sticker(chat_id=update.message.chat_id, sticker="CAACAgQAAxkBAAED8wxiDMYs52Ehx8uqh76tV-JocYlmqwAC5QADZprbKvN4A462THgxIwQ", reply_markup=ReplyKeyboardRemove())
            break
        except  Exception as e:
            time.sleep(1)
            location(update, context)

        # context.bot.send_message(chat_id=update.message.chat_id,text="opps! something went wrong please try again")

start_handler= CommandHandler("start",start)
echo_handler = MessageHandler(Filters.text, echo)
get_location_handler = CommandHandler("location", get_location)
location_handler = MessageHandler(Filters.location, location)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(get_location_handler)
dispatcher.add_handler(location_handler)
dispatcher.add_handler(echo_handler)

updater.start_polling(timeout=30,drop_pending_updates=False)

updater.idle()
