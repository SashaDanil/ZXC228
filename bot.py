import telebot
from telebot import types

API_TOKEN = '8032304693:AAH0e-7Oz3xfcOt2HNC95BRdIjDQ-j5xHSA'

bot = telebot.TeleBot(API_TOKEN)

main_menu = types.InlineKeyboardMarkup()
button_crypto = types.InlineKeyboardButton(text='Криптовалюта', callback_data='crypto')
button_fiat = types.InlineKeyboardButton(text='Валюты стран', callback_data='fiat')
button_info = types.InlineKeyboardButton(text='Информация о крипте', url='https://www.rbc.ru/crypto/')
main_menu.row(button_crypto, button_fiat)
main_menu.add(button_info)

crypto_menu = types.InlineKeyboardMarkup()
button_btc = types.InlineKeyboardButton(text='📈 Биткоин', url='https://www.rbc.ru/crypto/currency/btcusd')
button_eth = types.InlineKeyboardButton(text='🪙 Эфириум', url='https://www.rbc.ru/crypto/currency/ethusd')
button_xrp = types.InlineKeyboardButton(text='💸 XRP', url='https://www.rbc.ru/crypto/currency/xrpusd')
button_trump = types.InlineKeyboardButton(text='🙍‍♂️ TRUMP', url='https://ru.investing.com/crypto/official-trump')
button_back = types.InlineKeyboardButton(text='❌ Назад ❌', callback_data='back')
crypto_menu.add(button_btc, button_eth, button_xrp, button_trump)
crypto_menu.add(button_back)

fiat_menu = types.InlineKeyboardMarkup()
button_dollar = types.InlineKeyboardButton(text='🇺🇲 Доллар', url='https://www.rbc.ru/quote/ticker/72413')
button_euro = types.InlineKeyboardButton(text='🇪🇺 Евро', url='https://www.rbc.ru/quote/ticker/72383')
button_yuan = types.InlineKeyboardButton(text='🇨🇳 Юань', url='https://www.rbc.ru/quote/ticker/72377')
button_yen = types.InlineKeyboardButton(text='🇯🇵 Йен', url='https://ru.investing.com/currencies/jpy-rub')
fiat_menu.add(button_dollar, button_euro, button_yuan, button_yen)
fiat_menu.add(button_back)

@bot.message_handler(commands=['start'])
def handle_start(message):
    image_url = 'https://etoday.kz/wp-content/uploads/2023/04/Bitcoin-780x470.jpg'
    bot.send_photo(
        message.chat.id,
        image_url,
        caption='💵 Привет! Я бот для отслеживания курса криптовалют и валют. 🪙 Выберите категорию:',
        reply_markup=main_menu
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'crypto':
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption='Вы выбрали "Криптовалюту".',
            reply_markup=crypto_menu
        )
    elif call.data == 'fiat':
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption='Вы выбрали "Валюты стран".',
            reply_markup=fiat_menu
        )
    elif call.data == 'back':
        bot.edit_message_caption(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            caption='💵 Привет! Я бот для отслеживания курса криптовалют и валют. 🪙 Выберите категорию:',
            reply_markup=main_menu
        )

if __name__ == '__main__':
    bot.polling(none_stop=True)
