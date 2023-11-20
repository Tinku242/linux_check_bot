import subprocess
import telebot
from telebot import types
from dotenv import load_dotenv
import os
import time
import txtTOimg


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
    elif call.data == "services":
        service(call.message.chat.id)
    elif call.data == "whoami":
        whoami(call.message.chat.id)
    elif call.data == "shell":
        shell(call.message.chat.id)
    elif call.data == "shelltypes":
        shelltypes(call.message.chat.id)
    elif call.data == "uname":
        uname(call.message.chat.id)
    elif call.data == "list_files":
        listfiles(call.message.chat.id)
    elif call.data == "cmds":
        cmds(call.message.chat.id)
    elif call.data == "ipaddress":
        ip_address(call.message.chat.id)


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
    txtTOimg.textToimage(call, data, 600, 100)
    img = open(f"images/{call}.png", "rb")
    bot.send_photo(
        chat_id=chatid, photo=img, caption=call)


def docker_info(chatid, call):
    dockerinfo = subprocess.Popen(
        'sudo docker info', stdout=subprocess.PIPE, shell=True)
    (output, error) = dockerinfo.communicate()
    dockerinfo.wait()
    data = str(output.decode())
    txtTOimg.textToimage(call, data, 300, 900)
    img = open(f"images/{call}.png", "rb")
    bot.send_photo(
        chat_id=chatid, photo=img, caption=call)


#! SERVICES

services_markup = types.InlineKeyboardMarkup(row_width=2)
whoami = types.InlineKeyboardButton(
    text="who am i", callback_data="whoami")
shell = types.InlineKeyboardButton(
    text="shell", callback_data="shell")
shelltypes = types.InlineKeyboardButton(
    text="shell types", callback_data="shelltypes")
listfiles = types.InlineKeyboardButton(
    text="list files", callback_data="list_files")
uname = types.InlineKeyboardButton(
    text="uname", callback_data="uname")
services_markup.add(whoami, shell, shelltypes, listfiles, uname)


def service(chatid):
    bot.send_photo(chat_id=chatid, photo="https://linuxize.com/post/systemctl-list/featured_hu6e3ebb66d43d86b73d0155222f0e2af0_27589_768x0_resize_q75_lanczos.jpg",
                   caption="select the below commands to execute the cmds", reply_markup=services_markup)


def whoami(chatid):
    _whoami = subprocess.Popen(
        'whoami', stdout=subprocess.PIPE, shell=True)
    (output, error) = _whoami.communicate()
    _whoami.wait()
    data = str(output.decode())
    bot.send_message(chat_id=chatid, text=data)


def shell(chatid):
    _shell = subprocess.Popen(
        'which $SHELL', stdout=subprocess.PIPE, shell=True)
    (output, error) = _shell.communicate()
    _shell.wait()
    data = str(output.decode())
    bot.send_message(chat_id=chatid, text=data)


def shelltypes(chatid):
    _shells = subprocess.Popen(
        'cat /etc/shells', stdout=subprocess.PIPE, shell=True)
    (output, error) = _shells.communicate()
    _shells.wait()
    data = str(output.decode())
    bot.send_message(chat_id=chatid, text=data)


def uname(chatid):
    uname = subprocess.Popen(
        'uname -a', stdout=subprocess.PIPE, shell=True)
    (output, error) = uname.communicate()
    uname.wait()
    data = str(output.decode())
    bot.send_message(chat_id=chatid, text=data)


def listfiles(chatid):
    la = subprocess.Popen(
        'ls -a', stdout=subprocess.PIPE, shell=True)
    (output, error) = la.communicate()
    la.wait()
    data = str(output.decode())
    bot.send_message(chat_id=chatid, text=data)

#! cmd


cmds_markup = types.InlineKeyboardMarkup(row_width=2)
ipaddress = types.InlineKeyboardButton(
    text="ip addr", callback_data="ipaddress")
cmds_markup.add(ipaddress)


def cmds(chatid):
    bot.send_photo(chat_id=chatid, photo="https://imgs.search.brave.com/_dskMhbwpdtiuRgaERL3GuZjwLFhqf2xRzPt-vw2kfk/rs:fit:860:0:0/g:ce/aHR0cHM6Ly93d3cu/bGludXhzaGVsbHRp/cHMuY29tL3dwLWNv/bnRlbnQvdXBsb2Fk/cy8yMDIxLzEyL0xp/bnV4LUNvbW1hbmRz/LnBuZw",
                   caption="commands under the development", reply_markup=cmds_markup)


def ip_address(chatid):
    bot.send_message(chat_id=chatid, text="68.233.106.218")

#! NOT USER


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    msg = bot.reply_to(
        message=message, text=f"please use the buttons provided")
    time.sleep(10)
    bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)


bot.polling()
