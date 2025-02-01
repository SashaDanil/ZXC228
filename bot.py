from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = '8032304693:AAH0e-7Oz3xfcOt2HNC95BRdIjDQ-j5xHSA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

main_menu = InlineKeyboardMarkup()
button_crypto = InlineKeyboardButton('Криптовалюта', callback_data='crypto')
button_fiat = InlineKeyboardButton('Валюта стран', callback_data='fiat')
button_news = InlineKeyboardButton('Новости о криптовалюте', url='https://www.rbc.ru/crypto/')
main_menu.row(button_crypto, button_fiat)
main_menu.row(button_news)

crypto_menu = InlineKeyboardMarkup()
button_btc = InlineKeyboardButton('📈 Биткоин', url='https://www.rbc.ru/crypto/currency/btcusd')
button_eth = InlineKeyboardButton('🪙 Эфириум', url='https://www.rbc.ru/crypto/currency/ethusd')
button_xrp = InlineKeyboardButton('💸 XRP', url='https://www.rbc.ru/crypto/currency/xrpusd')
button_trump = InlineKeyboardButton('🙍‍♂️ TRUMP', url='https://ru.investing.com/crypto/official-trump')
button_back = InlineKeyboardButton('❌ Назад ❌', callback_data='back')
crypto_menu.row(button_btc)
crypto_menu.row(button_eth)
crypto_menu.row(button_xrp)
crypto_menu.row(button_trump)
crypto_menu.row(button_back)

fiat_menu = InlineKeyboardMarkup()
button_dollar = InlineKeyboardButton('🇺🇲 Доллар', url='https://www.rbc.ru/quote/ticker/72413')
button_euro = InlineKeyboardButton('🇪🇺 Евро', url='https://www.rbc.ru/quote/ticker/72383')
button_yuan = InlineKeyboardButton('🇨🇳 Юань', url='https://www.rbc.ru/quote/ticker/72377')
button_yen = InlineKeyboardButton('🇯🇵 Йена', url='https://ru.investing.com/currencies/jpy-rub')
button_back = InlineKeyboardButton('❌ Назад ❌', callback_data='back')
fiat_menu.row(button_dollar)
fiat_menu.row(button_euro)
fiat_menu.row(button_yuan)
fiat_menu.row(button_yen)
fiat_menu.row(button_back)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    image_url = 'https://etoday.kz/wp-content/uploads/2023/04/Bitcoin-780x470.jpg'
    await bot.send_photo(
        message.chat.id,
        photo=image_url,
        caption='💵 Привет, я бот для отслеживания крипты и валюты. 🪙 Выберите категорию:',
        reply_markup=main_menu
    )
@dp.callback_query_handler(lambda query: query.data in ['crypto', 'fiat', 'back'])
async def inline_callback(query: types.CallbackQuery):
    if query.data == 'crypto':
        await query.message.edit_caption(caption='Вы выбрали "Криптовалюту".', reply_markup=crypto_menu)
    elif query.data == 'fiat':
        await query.message.edit_caption(caption='Вы выбрали "Валюта стран".', reply_markup=fiat_menu)
    elif query.data == 'back':
        await query.message.edit_caption(caption='💵 Привет, я бот для отслеживания крипты и валюты. 🪙 Выберите категорию:', reply_markup=main_menu)
    
    await query.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
