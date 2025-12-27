import os
import discord
from discord.ext import commands
from googletrans import Translator
from flask import Flask
import threading

# -------- WEB SERVER (for Render + UptimeRobot) --------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_web).start()

# -------- DISCORD BOT --------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=None, intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

# -------- /help COMMAND (ENGLISH) --------
@bot.tree.command(name="help", description="How to use the translate bot")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**📘 Translate Bot – Help**\n\n"
        "**Usage:**\n"
        "`translate <language> <text>`\n\n"
        "**Example:**\n"
        "`translate sv hi what are you doing`\n\n"
        "**Result:**\n"
        "`@you hej vad gör du`\n\n"
        "**Language codes:**\n"
        "`sv` Swedish\n"
        "`en` English\n"
        "`de` German\n"
        "`fr` French\n"
        "`es` Spanish\n\n"
        "🗑 Your original message will be deleted automatically."
    )

# -------- MESSAGE LISTENER --------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if not message.content.lower().startswith("translate "):
        return

    parts = message.content.split(" ", 2)
    if len(parts) < 3:
        return

    target_lang = parts[1]
    text = parts[2]

    try:
        translated = translator.translate(text, dest=target_lang).text

        await message.delete()
        await message.channel.send(f"{message.author.mention} {translated}")

    except Exception as e:
        await message.channel.send("❌ Translation failed.")

bot.run(os.environ["DISCORD_TOKEN"])
