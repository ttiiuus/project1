import os

import requests

from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes



load_dotenv()

TOKEN = os.getenv("TOKEN")



def get_crypto_price(crypto: str) -> float:

    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd'

    response = requests.get(url)

    data = response.json()

    return data[crypto]['usd']



def get_crypto_news() -> list:

    url = 'https://api.coingecko.com/api/v3/news'

    response = requests.get(url)

    data = response.json()

    news = []

    for article in data[:3]: 

        news.append(f"{article['title']}\n{article['url']}")

    return news



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    keyboard = [

        [

            InlineKeyboardButton("Get Crypto Prices", callback_data='price'),

            InlineKeyboardButton("Get Crypto News", callback_data='news')

        ]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Hello, I am your bot. Choose an option:', reply_markup=reply_markup)



async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    query = update.callback_query

    await query.answer()

    btc_price = get_crypto_price('bitcoin')

    eth_price = get_crypto_price('ethereum')

    sol_price = get_crypto_price('solana')

    message = (

        f"NOW PRICE CRYPTO:\n"

        f"BTC: ${btc_price}\n"

        f"ETH: ${eth_price}\n"

        f"SOL: ${sol_price}"

    )

    await query.edit_message_text(message)



async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    query = update.callback_query

    await query.answer()

    news_list = get_crypto_news()

    message = "Crypto News:\n" + "\n\n".join(news_list)

    await query.edit_message_text(message)



if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(price, pattern='price'))

    application.add_handler(CallbackQueryHandler(news, pattern='news'))

    application.run_polling()


