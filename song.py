from HorridAPI import Songmrz
import os
from pyrogram import Client, filters
import aiohttp
from fastapi import FastAPI
from threading import Thread
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Telegram Bot configuration from environment variables
TOKEN = os.getenv("TOKEN")
API_ID = int(os.getenv("API_ID"))  # Ensure API_ID is an integer
API_HASH = os.getenv("API_HASH")

if not all([TOKEN, API_ID, API_HASH]):
    logger.error("Please set TOKEN, API_ID, and API_HASH in your .env file.")
    exit(1)

bot = Client(name="bot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)

# Horrid API configuration
api_key = os.getenv("API_KEY")
if not api_key:
    logger.error("Please set API_KEY in your .env file.")
    exit(1)

Horrid = Songmrz(api_key)

# FastAPI app setup
app = FastAPI()

# FastAPI root endpoint
@app.get("/")
async def root():
    return {"message": "Bot is working!"}

@app.get("/song/{song_name}")
async def get_song(song_name: str):
    logger.info(f"Received song request for: {song_name}")
    m = "Downloading song..."
    try:
        data = Horrid.download(song_name)
        url = data.url
        thumb_url = data.thumb
        title = data.title
        dura = data.duration
        songs = f"Title: {title}\nDuration: {dura}\nProvided by @Mrz_bots"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(f"{title}.mp3", "wb") as f:
                    f.write(await resp.read())  # Download song
            async with session.get(thumb_url) as resp:
                with open("thumb.jpg", "wb") as f:
                    f.write(await resp.read())  # Download thumbnail
        
        logger.info(f"Successfully downloaded and saved: {title}.mp3")
        return {
            "title": title,
            "duration": dura,
            "status": "Success",
            "files": {
                "song_file": f"{title}.mp3",
                "thumb_file": "thumb.jpg"
            }
        }
    except Exception as e:
        logger.error(f"Error occurred while processing the request: {e}")
        return {"error": "An error occurred while processing your request."}

# Telegram bot song handler
@bot.on_message(filters.command("song"))
async def song(client, message):
    if len(message.command) < 2:
        await message.reply("Give Any Song Name!")
        return

    query = " ".join(message.command[1:])
    m = await message.reply_text("📥 Downloading...")

    try:
        logger.info(f"Downloading song for query: {query}")
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
                    f.write(await resp.read())
            async with session.get(thumb_url) as resp:
                with open("thumb.jpg", "wb") as f:
                    f.write(await resp.read())

        await message.reply_audio(f"{title}.mp3", thumb="thumb.jpg", title=title, caption=songs)
        logger.info(f"Uploaded song: {title}")
    except Exception as e:
        await m.edit("An error occurred while processing your request.")
        logger.error(f"Error: {e}")

    await m.delete()

# Function to run the bot
def run_bot():
    bot.run()

# Run the bot and FastAPI app in separate threads
if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
