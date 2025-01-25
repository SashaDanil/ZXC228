import telebot
from telebot import types

API_TOKEN = '8032304693:AAH0e-7Oz3xfcOt2HNC95BRdIjDQ-j5xHSA'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Bitcoin', url='https://www.rbc.ru/crypto/currency/btcusd')
    itembtn2 = types.InlineKeyboardButton('Ethereum', url='https://www.rbc.ru/crypto/currency/ethusd')
    markup.add(itembtn1, itembtn2)
    
    image_url = 'https://etoday.kz/wp-content/uploads/2023/04/Bitcoin-780x470.jpg'
    
    bot.send_photo(message.chat.id, image_url, caption ='Привет, я бот для отслеживания крипты. Какую криптовалюту вы хотите узнать?', reply_markup=markup)

if __name__ == '__main__':
        bot.polling(none_stop=True)
