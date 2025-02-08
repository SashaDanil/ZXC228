import requests
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging

# Настройки API токена
API_TOKEN = '8032304693:AAH0e-7Oz3xfcOt2HNC95BRdIjDQ-j5xHSA'

# Создание экземпляра бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Главное меню
main_menu = InlineKeyboardMarkup()
button_crypto = InlineKeyboardButton('Криптовалюта', callback_data='crypto')
button_fiat = InlineKeyboardButton('Фиатная валюта', callback_data='fiat')
button_news = InlineKeyboardButton('Новости о криптовалюте', url='https://www.rbc.ru/crypto/')
button_video = InlineKeyboardButton('Трейдинг с нуля', url='https://rutube.ru/video/bba025514598fef2fda7b926d650d505/')
button_platforms = InlineKeyboardButton('Лучшие платформы', callback_data='platforms')
main_menu.row(button_crypto, button_fiat)
main_menu.row(button_platforms)
main_menu.row(button_video)
main_menu.row(button_news)

platforms_menu = InlineKeyboardMarkup()
button_binance = InlineKeyboardButton('Binance', url='https://binance.com')
button_kraken = InlineKeyboardButton('Kraken', url='https://kraken.com')
button_coinbase = InlineKeyboardButton('Coinbase', url='https://coinbase.com')
button_ftx = InlineKeyboardButton('FTX', url='https://ftx.com')
button_back_platforms = InlineKeyboardButton('❌ Назад ❌', callback_data='back_platforms')
platforms_menu.row(button_binance)
platforms_menu.row(button_kraken)
platforms_menu.row(button_coinbase)
platforms_menu.row(button_ftx)
platforms_menu.row(button_back_platforms)

# Меню для выбора криптовалюты
def crypto_menu():
    menu = InlineKeyboardMarkup()
    button_btc = InlineKeyboardButton('📈 Биткоин', callback_data='btc')
    button_eth = InlineKeyboardButton('🪙 Эфириум', callback_data='eth')
    button_xrp = InlineKeyboardButton('💸 XRP', callback_data='xrp')
    button_trump = InlineKeyboardButton('🙍‍♂️ BNB', callback_data='trump')
    button_back = InlineKeyboardButton('❌ Назад ❌', callback_data='back')
    menu.row(button_btc)
    menu.row(button_eth)
    menu.row(button_xrp)
    menu.row(button_trump)
    menu.row(button_back)
    return menu

# Меню для выбора фиатной валюты
fiat_menu = InlineKeyboardMarkup()
button_dollar = InlineKeyboardButton('🇺🇲 Доллар', callback_data='dollar')
button_euro = InlineKeyboardButton('🇪🇺 Евро', callback_data='euro')
button_yuan = InlineKeyboardButton('🇨🇳 Юань', callback_data='yuan')
button_yen = InlineKeyboardButton('🇰🇿 Тенге', callback_data='yen')
button_back_fiat = InlineKeyboardButton('❌ Назад ❌', callback_data='back_fiat')
fiat_menu.row(button_dollar)
fiat_menu.row(button_euro)
fiat_menu.row(button_yuan)
fiat_menu.row(button_yen)
fiat_menu.row(button_back_fiat)

async def get_currency_rate(currency):
    url = {
        'btc': 'https://www.rbc.ru/crypto/currency/btcusd',
        'eth': 'https://www.rbc.ru/crypto/currency/ethusd',
        'xrp': 'https://www.rbc.ru/crypto/currency/xrpusd',
        'trump': 'https://www.rbc.ru/crypto/currency/bnbusdt',
        'dollar': 'https://www.rbc.ru/quote/ticker/72413',
        'euro': 'https://www.rbc.ru/quote/ticker/338243',
        'yuan': 'https://www.rbc.ru/quote/ticker/59066',
        'yen': 'https://www.rbc.ru/quote/ticker/193076'
    }.get(currency)

    if not url:
        return 'Неизвестная валюта.'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                if currency in ['btc', 'eth', 'xrp', 'trump']:
                    rate_element = soup.find('div', class_='chart__subtitle')
                else:
                    rate_element = soup.find('span', class_='chart__info__sum')

                if rate_element:
                    rate = rate_element.text.strip()
                else:
                    rate = 'Курс недоступен.'
    except Exception as e:
        print(f"Ошибка при получении курса: {e}")
        rate = 'Произошла ошибка при получении курса.'

    return rate

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    image_url = 'https://etoday.kz/wp-content/uploads/2023/04/Bitcoin-780x470.jpg'
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption='💵 Привет, я бот для отслеживания крипты и валюты. 🪙 Выберите категорию:',
        reply_markup=main_menu
    )

@dp.callback_query_handler(lambda query: query.data in ['btc', 'eth', 'xrp', 'trump', 'dollar', 'euro', 'yuan', 'yen', 'crypto', 'fiat', 'back', 'back_crypto', 'back_fiat', 'platforms'])
async def inline_callback(query: types.CallbackQuery):
    if query.data in ['btc', 'eth', 'xrp', 'trump', 'dollar', 'euro', 'yuan', 'yen']:
        try:
            rate = await get_currency_rate(query.data)
            currency_names = {'btc': 'Bitcoin', 'eth': 'Ethereum', 'xrp': 'XRP', 'trump': 'BNB',
                              'dollar': 'Доллар', 'euro': 'Евро', 'yuan': 'Юань', 'yen': 'Тенге'}
            menu = crypto_menu() if query.data in ['btc', 'eth', 'xrp', 'trump'] else fiat_menu
            await query.message.edit_caption(
                caption=f"Текущий курс {currency_names[query.data]}: {rate}\n Выберите другую валюту или вернитесь назад:",
                reply_markup=menu
            )
        except Exception as e:
            await query.message.edit_caption(
                caption="Произошла ошибка при получении курса. Пожалуйста, попробуйте позже.",
                reply_markup=menu
            )
    elif query.data == 'crypto':
        await query.message.edit_caption(caption='Вы выбрали криптовалюту:', reply_markup=crypto_menu())
    elif query.data == 'fiat':
        await query.message.edit_caption(caption='Вы выбрали валюты стран:', reply_markup=fiat_menu)
    elif query.data == 'back':
        await query.message.edit_caption(caption='💵 Привет, я бот для отслеживания крипты и валюты. 🪙 Выберите категорию:', reply_markup=main_menu)
    elif query.data == 'platforms':
        platforms_message = (
            "Вот список некоторых из лучших платформ для торговли криптовалютой:\n"
            "-Binance - https://www.binance.com/ru \n"
            "-Coinbase - https://www.coinbase.com/ \n"
            "-Huobi Global - https://www.huobi.com/en-us/ \n"
            "-KuCoin - https://www.kucoin.com/ \n"
            "Каждая из них имеет свои особенности и преимущества. Выбирайте платформу, которая лучше всего соответствует вашим потребностям.\n\n"
        )
        back_button = InlineKeyboardButton(text='Закрыть', callback_data='close_platforms')
        back_keyboard = InlineKeyboardMarkup().add(back_button)
        await bot.send_message(chat_id=query.message.chat.id, text=platforms_message, reply_markup=back_keyboard)
    elif query.data in ['back_crypto', 'back_fiat']:
        await query.message.edit_caption(caption='💵 Привет, я бот для отслеживания крипты и валюты. 🪙 Выберите категорию:', reply_markup=main_menu)

@dp.callback_query_handler(lambda query: query.data == 'close_platforms')
async def close_platforms(query: types.CallbackQuery):
    await query.message.delete()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
