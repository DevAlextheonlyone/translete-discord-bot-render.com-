import discord
from discord.ext import commands
from googletrans import Translator
from flask import Flask
import threading
import os

# ---------- WEB SERVER ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running ✅"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ---------- DISCORD BOT ----------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.content.lower().startswith("translate "):
        return

    text = message.content[len("translate "):]

    try:
        translated = translator.translate(text, src="sv", dest="en").text
        await message.delete()
        await message.channel.send(f"**{message.author.display_name}:** {translated}")
    except Exception as e:
        await message.channel.send("❌ Translation failed")

bot.run(os.getenv("DISCORD_TOKEN"))
