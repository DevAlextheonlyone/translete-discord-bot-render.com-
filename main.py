import discord
from googletrans import Translator
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
translator = Translator()

@client.event
async def on_ready():
    print(f"Inloggad som {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()

    # kör bara om meddelandet börjar med "translate "
    if not content.lower().startswith("translate "):
        return

    text_to_translate = content[len("translate "):].strip()
    if not text_to_translate:
        return

    try:
        translated = translator.translate(
            text_to_translate,
            src="sv",
            dest="en"
        )

        await message.delete()

        await message.channel.send(
            f"**{message.author.display_name}:** {translated.text}"
        )

    except Exception as e:
        print("Fel:", e)

client.run(TOKEN)
