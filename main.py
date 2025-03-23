import os
import requests
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Load API keys from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
NUMVERIFY_API_KEY = os.getenv("NUMVERIFY_API_KEY")

# Replace these with your actual API credentials from my.telegram.org
API_ID = 14779203  # Replace with your API ID
API_HASH = "817abb4336a7581a29f3c14c55cab0e2"  # Replace with your API Hash

# Initialize Telegram bot
bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Logging
logging.basicConfig(level=logging.INFO)

# Function to check if a number is VoIP
def check_voip(phone_number):
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone_number}"
    response = requests.get(url).json()
    
    if response.get("valid"):
        if response.get("line_type") == "voip":
            return f"⚠️ The number {phone_number} is a **VoIP number**."
        else:
            return f"✅ The number {phone_number} is **not VoIP** (it's {response.get('line_type')})."
    else:
        return "❌ Invalid phone number. Please check and try again."

# Handle messages
@bot.on(events.NewMessage(pattern="/check (.+)"))
async def handler(event):
    phone_number = event.pattern_match.group(1)
    result = check_voip(phone_number)
    await event.reply(result)

# Start bot
print("Bot is running...")
bot.run_until_disconnected()

from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run():
    # Change the port to 5000 or 8000 (common for web servers)
    app.run(host='0.0.0.0', port=3000)

# Start the web server in a separate thread
Thread(target=run).start()
