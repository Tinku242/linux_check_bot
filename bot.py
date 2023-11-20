import subprocess
import telebot
from telebot import types
from dotenv import load_dotenv
import os
import time
import txtTOimg
from datetime import datetime


load_dotenv()

API_TOKEN = os.getenv("API_KEY")
bot = telebot.TeleBot(API_TOKEN)

#! on bot start initial message
bot.send_message(chat_id=5507592055, text="started")

#! Allowed User
ALLOWED_USER = os.getenv("ALLOWED_USER")

#! MAINMETHOD
main_menu_markup = types.InlineKeyboardMarkup(row_width=2)
docker = types.InlineKeyboardButton(
    text="docker  🐳🐳", callback_data="docker")
services = types.InlineKeyboardButton(
    text="services  ⚙️⚙️", callback_data="services")
cmds = types.InlineKeyboardButton(
    text="cmds 💻💻", callback_data="cmds")
main_menu_markup.add(docker, services, cmds)


@bot.message_handler(commands=['start'])
def welcome_msg(message):
    if str(ALLOWED_USER) == str(message.chat.id):
        text = "*Linux server* 🐧🐧🐧"
        msg = bot.send_message(chat_id=message.chat.id,
                               text=text, reply_markup=main_menu_markup, parse_mode='Markdown')
    else:
        msg = bot.send_message(chat_id=message.chat.id, text="not allowed")


@bot.callback_query_handler(func=lambda call: True)
def main_inline_callback(call):
    if call.data == "docker":
        docker(call.message.chat.id)
    elif call.data == "docker_ps":
        docker_ps(call.message.chat.id, call.data)
    elif call.data == "docker_images":
        docker_images(call.message.chat.id, call.data)
    elif call.data == "docker_info":
        docker_info(call.message.chat.id, call.data)


#! DOCKER
docker_markup = types.InlineKeyboardMarkup(row_width=2)
docker_ps = types.InlineKeyboardButton(
    text="docker ps", callback_data="docker_ps")
docker_images = types.InlineKeyboardButton(
    text="docker Images", callback_data="docker_images")
docker_info = types.InlineKeyboardButton(
    text="docker info", callback_data="docker_info")
docker_markup.add(docker_ps, docker_images, docker_info)


def docker(chatid):
    bot.send_photo(chat_id=chatid, photo="https://imgs.search.brave.com/Y09WHvoJ_r_FAjMS_Z_imQz-qXQaUCiQV-U2UvQH8rk/rs:fit:860:0:0/g:ce/aHR0cHM6Ly9kZXZv/cHNjdWJlLmNvbS93/cC1jb250ZW50L3Vw/bG9hZHMvMjAyMS8w/NC9Db3B5LW9mLWNv/bnRhaW5lci1ydW5u/aW5nLTEtbWluLTEt/NTYweDI3NS5wbmc",
                   caption="select the below commands to execute the docker cmds", reply_markup=docker_markup)


def docker_ps(chatid, call):
    dockerps = subprocess.Popen(
        'sudo docker ps', stdout=subprocess.PIPE, shell=True)
    (output, errors) = dockerps.communicate()
    dockerps.wait()
    data = str(output.decode())
    txtTOimg.textToimage(call, data, 900, 100)
    img = open(f"images/{call}.png", "rb")
    bot.send_photo(
        chat_id=chatid, photo=img, caption=call)


def docker_images(chatid, call):
    dockerimages = subprocess.Popen(
        'sudo docker images', stdout=subprocess.PIPE, shell=True)
    (output, error) = dockerimages.communicate()
    dockerimages.wait()
    data = str(output.decode())
    txtTOimg(data, 600, 200)
    img = open(f"images/{call}.png", "rb")
    bot.send_photo(
        chat_id=chatid, photo=img, caption=call)


def docker_info(chatid, call):
    dockerinfo = subprocess.Popen(
        'sudo docker info', stdout=subprocess.PIPE, shell=True)
    (output, error) = dockerinfo.communicate()
    dockerinfo.wait()
    data = str(output.decode())
    txtTOimg(data, 300, 900)
    img = open(f"images/{call}.png", "rb")
    bot.send_photo(
        chat_id=chatid, photo=img, caption=call)


#! NOT USER
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    msg = bot.reply_to(
        message=message, text=f"please use the buttons provided")
    time.sleep(10)
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)


bot.polling()
