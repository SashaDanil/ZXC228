import telebot

API_TOKEN = '8032304693:AAH0e-7Oz3xfcOt2HNC95BRdIjDQ-j5xHSA'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "dfgasdfasdf")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling(none_stop=True)