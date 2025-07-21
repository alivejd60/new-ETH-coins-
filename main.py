import telebot
import requests

BOT_TOKEN = "7429771746:AAFjHfG5HW3IgXtYG0SlLM0yVGOkZQyJUe8"
CHAT_ID = "@alivejd60"
bot = telebot.TeleBot(BOT_TOKEN)

def get_new_tokens():
    # Example dummy data (replace with real ETH token tracking logic)
    return [
        {
            "name": "TestToken",
            "address": "0x123456789...",
            "liquidity": "$12,000",
            "market_cap": "$50,000",
            "risk": "Low"
        }
    ]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "ETH New Token Bot Active!")

@bot.message_handler(commands=['check'])
def send_tokens(message):
    tokens = get_new_tokens()
    for token in tokens:
        msg = (
            f"🆕 New ETH Token\n"
            f"Name: {token['name']}\n"
            f"Address: `{token['address']}`\n"
            f"Liquidity: {token['liquidity']}\n"
            f"Market Cap: {token['market_cap']}\n"
            f"Risk: {token['risk']}"
        )
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")

bot.polling()
