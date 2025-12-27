import os
import discord
from discord.ext import commands
from googletrans import Translator

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

    # Kräver att man skriver "translate"
    if not content.lower().startswith("translate "):
        return

    parts = content.split(" ", 2)

    # translate sv text
    if len(parts) < 3:
        await message.delete()
        await message.channel.send(
            "❌ **Fel format**\n"
            "**Exempel:** `translate sv hello how are you`"
        )
        return

    _, target_lang, text = parts

    try:
        result = translator.translate(text, dest=target_lang)
        await message.delete()
        await message.channel.send(result.text)

    except Exception:
        await message.delete()
        await message.channel.send("❌ Kunde inte översätta texten.")


@bot.tree.command(name="help", description="Hur du använder translate-botten")
async def help_command(interaction: discord.Interaction):
    await interaction.response.send_message(
        "**📘 Translate Bot – Hjälp**\n\n"
        "**Användning:**\n"
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
        "🔹 Ditt meddelande tas bort automatiskt."
    )


async def setup_hook():
    await bot.tree.sync()


bot.setup_hook = setup_hook
bot.run(TOKEN)
