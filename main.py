import os
import time
import requests
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

ETHERSCAN_API = "https://api.dexscreener.com/latest/dex/pairs/ethereum"

def is_legit_token(token):
    try:
        liquidity = float(token.get("liquidity", {}).get("usd", 0))
        market_cap = float(token.get("fdv", 0))
        honeypot = "?"  # Placeholder for honeypot check
        locked = token.get("liquidity", {}).get("lock", {}).get("isLocked", False)

        return liquidity >= 10000 and market_cap <= 1000000 and locked is True
    except:
        return False

def fetch_tokens():
    try:
        response = requests.get(ETHERSCAN_API)
        data = response.json().get("pairs", [])
        return data
    except Exception as e:
        print("Fetch error:", e)
        return []

def send_alert(token):
    name = token.get("baseToken", {}).get("name")
    symbol = token.get("baseToken", {}).get("symbol")
    address = token.get("baseToken", {}).get("address")
    price = token.get("priceUsd")
    market_cap = token.get("fdv")
    liquidity = token.get("liquidity", {}).get("usd")
    pair_link = token.get("url", "N/A")

    msg = f"""
🚀 *New ETH Token Detected*
*Name:* {name} ({symbol})
*Address:* `{address}`
💧 *Liquidity:* ${liquidity}
📈 *Market Cap:* ${market_cap}
🔗 [View Chart]({pair_link})
"""
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown", disable_web_page_preview=True)

def run_bot():
    seen = set()

    while True:
        tokens = fetch_tokens()
        for token in tokens:
            address = token.get("baseToken", {}).get("address")
            if address not in seen and is_legit_token(token):
                send_alert(token)
                seen.add(address)
        time.sleep(60)

if __name__ == "__main__":
    run_bot()
