from HorridAPI import Songmrz
import os
from pyrogram import Client, filters
import aiohttp
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
TOKEN = os.getenv("TOKEN")
API_ID = int(os.getenv("API_ID"))  # API_ID must be an integer
API_HASH = os.getenv("API_HASH")
API_KEY = os.getenv("API_KEY")

# Check if all necessary environment variables are loaded
if not all([TOKEN, API_ID, API_HASH, API_KEY]):
    raise ValueError("Missing environment variables. Please check your .env file.")

# Initialize the bot and the API
bot = Client(name="bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
Horrid = Songmrz(API_KEY)

@bot.on_message(filters.command(["song", "play", "played"]))
async def song(client, message):
    if len(message.command) < 2:
        await message.reply("Give Any Song Name!")
        return

    query = " ".join(message.command[1:])
    m = await message.reply_text("📥 Downloading...")

    try:
        data = Horrid.download(query)
        url = data.url
        thumb_url = data.thumb
        title = data.title
        dura = data.duration
        songs = f"Title: {title}\nDuration: {dura}\nProvided by @Mrz_bots"

        await m.edit("📤 Uploading...")
        await message.reply_photo(photo=thumb_url, caption=songs)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(f"{title}.mp3", "wb") as f:
                    f.write(await resp.read())  # Use await resp.read() to download the song
            async with session.get(thumb_url) as resp:
                with open("thumb.jpg", "wb") as f:
                    f.write(await resp.read())  # Download the thumbnail

        await message.reply_audio(f"{title}.mp3", thumb="thumb.jpg", title=title, caption=songs)
    except Exception as e:
        await m.edit("An error occurred while processing your request.")
        print(f"Error: {e}")  # Log the error for debugging

    await m.delete()

print("Bot is working")
bot.run()
