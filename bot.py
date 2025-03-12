import requests
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

API_TOKEN = '8032304693:AAH0e-7Oz3xfcOt2HNC95BRdIjDQ-j5xHSA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

main_menu = InlineKeyboardMarkup()
button_crypto = InlineKeyboardButton('🪙Криптовалюта🪙', callback_data='crypto')
button_fiat = InlineKeyboardButton('💰Валюта стран💰', callback_data='fiat')
button_video = InlineKeyboardButton('🚀Трейдинг с нуля🚀', callback_data='video')
button_platforms = InlineKeyboardButton('👍Лучшие платформы👍', callback_data='platforms')
main_menu.row(button_crypto, button_fiat)
main_menu.row(button_platforms)
main_menu.row(button_video)

plat_menu = InlineKeyboardMarkup()
button_bin = InlineKeyboardButton(text='Binance', url='https://www.binance.com/ru')
button_byb = InlineKeyboardButton(text='Bybit', url='https://www.bybit.com/en-US/')
button_coin = InlineKeyboardButton(text='Coinbase', url='https://www.coinbase.com/ru/exchange')
button_okx = InlineKeyboardButton(text='OKX', url='https://www.okx.com/ru')
button_back_plat = InlineKeyboardButton('❌ Назад ❌', callback_data='back_plat')
plat_menu.row(button_bin)
plat_menu.row(button_byb)
plat_menu.row(button_coin)
plat_menu.row(button_okx)
plat_menu.row(button_back_plat)

def crypto_menu():
    menu = InlineKeyboardMarkup()
    button_btc = InlineKeyboardButton('📈 Bitcoin', callback_data='btc')
    button_eth = InlineKeyboardButton('🪙 Ethereum', callback_data='eth')
    button_xrp = InlineKeyboardButton('💸 Toncoin', callback_data='xrp')
    button_bnb = InlineKeyboardButton('🙍‍♂️ Dogecoin', callback_data='doge')  
    button_back = InlineKeyboardButton('❌ Назад ❌', callback_data='back')
    menu.row(button_btc)
    menu.row(button_eth)
    menu.row(button_xrp)
    menu.row(button_bnb)
    menu.row(button_back)
    return menu

def fiat_menu():
    fiat_menu_mm = InlineKeyboardMarkup()
    button_dollar = InlineKeyboardButton('🇺🇲 Доллар', callback_data='dollar')
    button_euro = InlineKeyboardButton('🇪🇺 Евро', callback_data='euro')
    button_yuan = InlineKeyboardButton('🇯🇵 Йена', callback_data='yuan')
    button_yen = InlineKeyboardButton('🇰🇿 Тенге', callback_data='yen')
    button_back_fiat = InlineKeyboardButton('❌ Назад ❌', callback_data='back_fiat')
    fiat_menu_mm.row(button_dollar)
    fiat_menu_mm.row(button_euro)
    fiat_menu_mm.row(button_yuan)
    fiat_menu_mm.row(button_yen)
    fiat_menu_mm.row(button_back_fiat)
    return fiat_menu_mm  

@dp.callback_query_handler(lambda query: query.data == 'video')
async def send_local_video(callback_query: CallbackQuery):
    file_path = r'Трейдинг_с_нуля__самое_ПРОСТОЕ_объяснение_каждого_элемента.mp4'
    
    if not os.path.exists(file_path):
        await callback_query.message.reply("Файл не найден.")
        return
    
    try:
        with open(file_path, 'rb') as video:
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton(text="Закрыть", callback_data="close1")
            )
            await callback_query.message.answer_video(video, caption='Это видео кратко расскажет вам, про трейдинг.', reply_markup=keyboard)
    except Exception as e:
        await callback_query.message.reply("Произошла ошибка при попытке отправить видео.")
        logging.error(f"Ошибка при открытии файла: {file_path}. Ошибка: {e}")

@dp.callback_query_handler(lambda query: query.data == 'close1')
async def close_message(callback_query: CallbackQuery):
    await callback_query.message.delete()

async def get_currency_rate(currency):
    url_map = {
        'btc': 'https://www.okx.com/ru/price/bitcoin-btc',  
        'eth': 'https://www.okx.com/ru/price/ethereum-eth',  
        'xrp': 'https://www.okx.com/ru/price/toncoin-ton',  
        'doge': 'https://www.okx.com/ru/price/dogecoin-doge',  
        'dollar': 'https://www.banki.ru/products/currency/usd/',
        'euro': 'https://www.banki.ru/products/currency/eur/',
        'yuan': 'https://www.banki.ru/products/currency/cash/jpy/moskva/',
        'yen': 'https://www.banki.ru/products/currency/cash/kzt/moskva/'  
    }

    url = url_map.get(currency)

    if not url:
        return f'Валюта "{currency}" неизвестна или отсутствует в списке.'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                
                if currency in ['btc', 'eth', 'xrp', 'doge']:  
                    rate_element = soup.find('div', class_='index_price__VXAhl')  
                elif currency in ['dollar', 'euro', 'yuan', 'yen']:  
                    rate_element = soup.find('div', class_='Flexbox__sc-1yjv98p-0 feZtEw')  
                
                if rate_element:
                    rate = rate_element.get_text(strip=True)
                else:
                    rate = 'Информация недоступна.'
    except Exception as e:
        logging.error(f"Ошибка при получении данных: {e}")
        rate = 'Произошла ошибка при получении информации.'

    return rate

async def main():
    tasks = [
        get_currency_rate('btc'),
        get_currency_rate('eth'),
        get_currency_rate('xrp'),
        get_currency_rate('doge'),
        get_currency_rate('dollar'),
        get_currency_rate('euro'),
        get_currency_rate('yuan'),
        get_currency_rate('yen')
    ]

    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    image_url = 'https://etoday.kz/wp-content/uploads/2023/04/Bitcoin-780x470.jpg'
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=image_url,
        caption='💵 Привет, я бот для отслеживания крипты и валюты. 🪙 Выберите категорию:',
        reply_markup=main_menu
    )

@dp.callback_query_handler(lambda query: query.data in ['btc', 'eth', 'xrp', 'doge', 'dollar', 'euro', 'yuan', 'yen', 'crypto', 'fiat', 'back', 'back_fiat', 'platforms', 'back_plat'])
async def inline_callback(query: types.CallbackQuery):
    if query.data in ['btc', 'eth', 'xrp', 'doge', 'dollar', 'euro', 'yuan', 'yen']:
        try:
            rate = await get_currency_rate(query.data)
            currency_names = {
                'btc': 'Bitcoin',
                'eth': 'Ethereum',
                'xrp': 'Toncoin',
                'doge': 'Dogecoin',
                'dollar': 'Доллар',
                'euro': 'Евро',
                'yuan': 'Йена',
                'yen': 'Тенге'
            }
            
            menu = crypto_menu() if query.data in ['btc', 'eth', 'xrp', 'doge'] else fiat_menu()
            
            if query.data in ['dollar', 'euro', 'yuan', 'yen']:  
                caption = (
                    f"Текущий курс {currency_names[query.data]}: {rate}\n"
                    "Этот курс в Москве, если вы хотите узнать курс в своём городе, переходите по ссылке: https://www.banki.ru/\n"
                    "Выберите другую валюту или вернитесь назад:"
                )
            else:  
                caption = (
                    f"Текущий курс {currency_names[query.data]}: {rate}\n"
                    "Выберите другую валюту или вернитесь назад:"
                )
            
            await query.message.edit_caption(caption=caption, reply_markup=menu)
        except Exception as e:
            logging.error(f"Ошибка: {e}")
            
            menu = crypto_menu() if query.data in ['btc', 'eth', 'xrp', 'doge'] else fiat_menu()
            await query.message.edit_caption(
                caption="Произошла ошибка при получении курса. Пожалуйста, попробуйте позже.",
                reply_markup=menu
            )
    elif query.data == 'crypto':
        await query.message.edit_caption(caption='Вы выбрали криптовалюту:', reply_markup=crypto_menu())
    elif query.data == 'fiat':
        await query.message.edit_caption(caption='Вы выбрали валюты стран:', reply_markup=fiat_menu())
    elif query.data == 'platforms':
        await query.message.edit_caption(caption='Лучшие платформы для покупки и продажи крипты', reply_markup=plat_menu)
    elif query.data in ['back', 'back_plat', 'back_fiat']:
        await query.message.edit_caption(caption='💵 Привет, я бот для отслеживания крипты и валюты. 🪙 Выберите категорию:', reply_markup=main_menu)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
