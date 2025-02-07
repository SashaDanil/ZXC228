from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import logging

API_TOKEN = '8032304693:AAH0e-7Oz3xfcOt2HNC95BRdIjDQ-j5xHSA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Главная клавиатура
main_menu = InlineKeyboardMarkup()
button_crypto = InlineKeyboardButton('Криптовалюта', callback_data='crypto')
button_fiat = InlineKeyboardButton('Валюта стран', callback_data='fiat')
button_news = InlineKeyboardButton('Новости о криптовалюте', url='https://www.rbc.ru/crypto/')
button_video = InlineKeyboardButton('Трейдинг с нуля', url='https://rutube.ru/video/bba025514598fef2fda7b926d650d505/')
button_platforms = InlineKeyboardButton('Лучшие платформы', callback_data='platforms')
main_menu.row(button_crypto, button_fiat)
main_menu.row(button_platforms)
main_menu.row(button_video)
main_menu.row(button_news)

# Клавиатура для криптовалюты
crypto_menu = InlineKeyboardMarkup()
button_btc = InlineKeyboardButton('📈 Биткоин', url='https://www.rbc.ru/crypto/currency/btcusd')
button_eth = InlineKeyboardButton('🪙 Эфириум', url='https://www.rbc.ru/crypto/currency/ethusd')
button_xrp = InlineKeyboardButton('💸 XRP', url='https://www.rbc.ru/crypto/currency/xrpusd')
button_trump = InlineKeyboardButton('🙍‍♂️ TRUMP', url='https://ru.investing.com/crypto/official-trump')
button_back_crypto = InlineKeyboardButton('❌ Назад ❌', callback_data='back_crypto')
crypto_menu.row(button_btc)
crypto_menu.row(button_eth)
crypto_menu.row(button_xrp)
crypto_menu.row(button_trump)
crypto_menu.row(button_back_crypto)

# Клавиатура для фиатных валют
fiat_menu = InlineKeyboardMarkup()
button_dollar = InlineKeyboardButton('🇺🇲 Доллар', url='https://www.rbc.ru/quote/ticker/72413')
button_euro = InlineKeyboardButton('🇪🇺 Евро', url='https://www.rbc.ru/quote/ticker/72383')
button_yuan = InlineKeyboardButton('🇨🇳 Юань', url='https://www.rbc.ru/quote/ticker/72377')
button_yen = InlineKeyboardButton('🇯🇵 Йена', url='https://ru.investing.com/currencies/jpy-rub')
button_back_fiat = InlineKeyboardButton('❌ Назад ❌', callback_data='back_fiat')
fiat_menu.row(button_dollar)
fiat_menu.row(button_euro)
fiat_menu.row(button_yuan)
fiat_menu.row(button_yen)
fiat_menu.row(button_back_fiat)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    image_url = 'https://etoday.kz/wp-content/uploads/2023/04/Bitcoin-780x470.jpg'
    logging.info("Команда /start обработана.")
    # Сохраняем сообщение для дальнейшего редактирования
    await bot.send_photo(
        message.chat.id,
        photo=image_url,
        caption='💵 Привет, я бот для отслеживания крипты и валюты. 🪙 Выберите категорию:',
        reply_markup=main_menu
    )

# Обработчик коллбэков
@dp.callback_query_handler(lambda query: query.data in ['crypto', 'fiat', 'back_crypto', 'back_fiat', 'platforms'])
async def inline_callback(query: types.CallbackQuery):
    if query.data == 'crypto':
        await query.message.edit_caption(caption='Вы выбрали "Криптовалюту".', reply_markup=crypto_menu)
    elif query.data == 'fiat':
        await query.message.edit_caption(caption='Вы выбрали "Валюта стран".', reply_markup=fiat_menu)
    elif query.data == 'platforms':
        platforms_message = (
            "Вот список некоторых из лучших платформ для торговли криптовалютой:\n"
            "- Binance\n"
            "- Coinbase\n"
            "- Kraken\n"
            "- Huobi Global\n"
            "- KuCoin\n"
            "Каждая из них имеет свои особенности и преимущества. Выбирайте платформу, которая лучше всего соответствует вашим потребностям.\n\n"
        )
        back_button = InlineKeyboardButton(text='Закрыть', callback_data='close_platforms')
        back_keyboard = InlineKeyboardMarkup().add(back_button)
        await bot.send_message(chat_id=query.message.chat.id, text=platforms_message, reply_markup=back_keyboard)
    elif query.data == 'back_crypto':
        await return_to_main_menu(query)
    elif query.data == 'back_fiat':
        await return_to_main_menu(query)

# Функция возврата к главному меню
async def return_to_main_menu(query: types.CallbackQuery):
    await query.message.edit_caption(reply_markup=main_menu)

# Обработчик кнопки "Закрыть"
@dp.callback_query_handler(lambda query: query.data == 'close_platforms')
async def close_platforms(query: types.CallbackQuery):
    await query.message.delete()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
