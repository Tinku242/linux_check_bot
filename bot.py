import telebot
from telebot import types
from dotenv import load_dotenv
import os
import time
import schedule


load_dotenv()

API_TOKEN = os.getenv("API_KEY")
bot = telebot.TeleBot(API_TOKEN)
bot.send_message(chat_id=5507592055, text="started")

ALLOWED_USER = os.getenv("ALLOWED_USER")
main_menu_markup = types.InlineKeyboardMarkup(row_width=2)
google = types.InlineKeyboardButton(
    text="google", callback_data="google")
google1 = types.InlineKeyboardButton(
    text="google", url="www.google.com")
google2 = types.InlineKeyboardButton(
    text="google", url="www.google.com")
main_menu_markup.add(google, google1, google2)


@bot.message_handler(commands=['start'])
def welcome_msg(message):
    if str(ALLOWED_USER) == str(message.chat.id):
        text = "*Linux server*"
        msg = bot.send_message(chat_id=message.chat.id,
                               text=text, reply_markup=main_menu_markup, parse_mode='Markdown')
    else:
        msg = bot.send_message(chat_id=message.chat.id, text="not allowed")
    time.sleep(10)
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callback(call):
    if call.data == "google":
        bot.send_message(call.message.chat.id, "www.google.com")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    msg = bot.reply_to(
        message=message, text=f"please use the buttons provided {message.chat.id}")
    time.sleep(10)
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)


next_time = time.time()
while True:
    bot.send_message(chat_id=5507592055,
                     text=f"time interval {time.asctime(time.localtime(time.time()))}")
    next_time += 60
    time.sleep(max(0, next_time - time.time()))

bot.polling()
