import requests
import time
from telegram import Bot

# === CONFIG ===
TELEGRAM_TOKEN = "PASTE-YOUR-BOT-TOKEN-HERE"
CHAT_ID = "@Alivejd60"  # Can also be your Telegram ID if not using a channel
bot = Bot(token=TELEGRAM_TOKEN)

# === SETTINGS ===
CHECK_INTERVAL = 15  # seconds
ETHERSCAN_API = "https://api.dexscreener.com/latest/dex/pairs/ethereum"

# === FAKE DATABASE to avoid duplicates ===
seen_tokens = set()

def get_new_tokens():
    try:
        response = requests.get(ETHERSCAN_API)
        data = response.json()
        pairs = data.get("pairs", [])
        new_ones = []

        for pair in pairs:
            if pair["pairAddress"] not in seen_tokens:
                if pair["chainId"] == "eth":
                    new_ones.append(pair)
                    seen_tokens.add(pair["pairAddress"])
        return new_ones
    except Exception as e:
        print(f"Error fetching pairs: {e}")
        return []

def send_alert(token):
    try:
        name = token.get("baseToken", {}).get("name", "Unknown")
        address = token.get("pairAddress", "N/A")
        mc = token.get("fdv", "Unknown")
        liquidity = token.get("liquidity", {}).get("usd", "Unknown")

        message = f"""🚨 *New Ethereum Token Detected* 🚨

🪙 *Name:* {name}
🔗 *Address:* `{address}`
📈 *Market Cap:* ${mc}
💧 *Liquidity:* ${liquidity}

🧪 *Honeypot:* Checking...
🔒 *LP Locked:* Checking...
👥 *Holder Risk:* TBD

🕒 Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"Error sending message: {e}")

while True:
    new_tokens = get_new_tokens()
    for token in new_tokens:
        send_alert(token)
    time.sleep(CHECK_INTERVAL)
