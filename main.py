import os
import threading
import discord
from discord.ext import commands
from googletrans import Translator
from flask import Flask

# =====================
# 🌐 WEB SERVER
# =====================
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Discord Translate Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_web).start()

# =====================
# 🤖 DISCORD BOT
# =====================
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
translator = Translator()

@bot.event
async def on_ready():
    print(f"✅ Inloggad som {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()

    # Kräver "translate"
    if not content.lower().startswith("translate "):
        return

    parts = content.split(" ", 2)

    # translate sv text
    if len(parts) < 3:
        await message.delete()
        await message.channel.send(
            "❌ **Fel format**\n"
            "**Exempel:** `translate sv hi how are you`"
        )
        return

    _, target_lang, text = parts

    try:
        result = translator.translate(text, dest=target_lang)
        await message.delete()
        await message.channel.send(result.text)

    except Exception:
        await message.delete()
        await message.channel.send("❌ Kunde inte översätta.")

@bot.tree.command(name="help", description="Hur du använder translate-botten")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**📘 Translate Bot – Hjälp**\n\n"
        "**Format:**\n"
        "`translate <språk> <text>`\n\n"
        "**Exempel:**\n"
        "`translate sv hi what are you doing`\n\n"
        "**Resultat:**\n"
        "`hej vad gör du`\n\n"
        "**Språkförkortningar:**\n"
        "`sv` svenska\n"
        "`en` engelska\n"
        "`de` tyska\n"
        "`fr` franska\n"
        "`es` spanska\n\n"
        "🗑 Ditt meddelande tas bort automatiskt."
    )

async def setup_hook():
    await bot.tree.sync()

bot.setup_hook = setup_hook
bot.run(TOKEN)
