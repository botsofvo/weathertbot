from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import os
from test import get_forecasts
from createpage import pagecreator
# check for  new message from api -> polling
updater = Updater(token=os.getenv('API_KEY'))

#allows to reginster handler -> command, text, video , audio etc
dispatcher = updater.dispatcher

# define a command callback funtion
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text = " Hello 🙋  nice to meet you, here are commands 🗒️ you can send me 🔺 and get the replys 🔻 as follows:\n1./location - Send your current location and I will send you 24hr forecast⛅.")
# create a command handler 
start_handler= CommandHandler("start",start)

dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="'"+update.message.text+"'\n- by "+update.message.from_user.name)

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
    button1= [[InlineKeyboardButton(text="click here",url=pagelink)]]
    reply_markup1 = InlineKeyboardMarkup(button1)
    # f=open("animated_sticker.tgs", 'rb')
    context.bot.send_message(chat_id=update.message.chat_id,text="😃 Here is your weather forecast:", reply_markup=reply_markup1,parse_mode='html')
    # context.bot.send_message(chat_id=update.message.chat_id,text="😊Thanks for using....\n 👀See menu button for more commands",
    #                          reply_markup=ReplyKeyboardRemove())
    context.bot.send_sticker(chat_id=update.message.chat_id, sticker="CAACAgUAAxkBAAED7ctiCoQrncbFSOtIw46b_5dFjvHEMQACAwAD5UvxN-gmo43ymUmCIwQ", reply_markup=ReplyKeyboardRemove())
    # context.bot.send_message(chat_id=update.message.chat_id,
    #                          text=forecasts,
    #                          reply_markup=ReplyKeyboardRemove())


location_handler = MessageHandler(Filters.location, location)
dispatcher.add_handler(location_handler) 






dispatcher.add_handler(echo_handler)
# start polling 
updater.start_polling()
