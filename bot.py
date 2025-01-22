import telebot 

bot = telebot.TeleBot('8032304693:AAH0e-7Oz3xfcOt2HNC95BRdIjDQ-j5xHSA')

@bot.message_handler(commands=['start'])
def send_welcome (message):
    bot.reply_to(message, text= "Привет,я бот для отслеживания крипты")
    bot.reply_to(message, text= "Какую ты хочешь крипту узнать?")
bot.polling(none_stop=True)
