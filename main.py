from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
from test import get_forecasts
# check for  new message from api -> polling
updater = Updater(token=os.getenv('API_KEY'))

#allows to reginster handler -> command, text, video , audio etc
dispatcher = updater.dispatcher

# define a command callback funtion
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text = "hello nice to meet you.")
# create a command handler 
start_handler= CommandHandler("start",start)

dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text) 

echo_handler = MessageHandler(Filters.text, echo)



def option(update, context):
    button = [
        [InlineKeyboardButton("option 1", callback_data="1"),
        InlineKeyboardButton("option 2", callback_data="2")],
        [InlineKeyboardButton("option 3", callback_data="3")]
    ]
    reply_markup= InlineKeyboardMarkup(button)

    context.bot.send_message(chat_id=update.message.chat_id, text="Choose one option..", reply_markup=reply_markup)

option_handler = CommandHandler("option",option)
# add command handler to dispatcher 
dispatcher.add_handler(option_handler)

def button(update, context):
    query = update.callback_query
    context.bot.edit_message_text(chat_id=query.message.chat_id,
    text="thanks for choosing {}.".format(query.data),message_id=query.message.message_id)

button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)

def get_location(update, context):
    button = [
        [KeyboardButton("Share location", request_location=True)]
        ]
    reply_markup = ReplyKeyboardMarkup(button)
    context.bot.send_message(chat_id=update.message.chat_id,
    text="Mind sharing location?",
    reply_markup=reply_markup)

get_location_handler = CommandHandler("location", get_location)
dispatcher.add_handler(get_location_handler)

def location(update, context):
    lat = update.message.location.latitude
    lon = update.message.location.longitude
    forecasts = get_forecasts(lat, lon)
    context.bot.send_message(chat_id=update.message.chat_id,
    text=forecasts,
    reply_markup= ReplyKeyboardRemove())

location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler) 






dispatcher.add_handler(echo_handler)
# start polling 
updater.start_polling()
