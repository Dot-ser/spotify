import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get credentials from environment variables
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize the bot client
app = Client("instagram_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command(["instadl", "insdl", "insta", "instadownload"]))
async def igdownload(client, message):
    if len(message.command) < 2:
        return await message.reply_text("**Please provide an Instagram URL 🤦‍♂️**")
    
    url = message.text.split(None, 1)[1]
    msg = await message.reply_text("**Downloading 📤**")
    
    try:
        # Add a timeout to avoid hanging requests
        response = requests.get(f"https://horridapi.onrender.com/instadl?url={url}", timeout=60)
        data = response.json()
    except requests.exceptions.RequestException as e:
        await msg.edit_text(f"**Error contacting API: {str(e)}**")
        return
    
    # Check if the API response is OK
    if not data.get("STATUS") == "OK":
        await message.reply_text("**Not a valid Instagram URL 🤷‍♂️**")
        await msg.delete()
        return
    
    result = data.get("result", [])
    
    # Prepare the media list for Telegram
    media = []
    for s in result:                
        if s["media"] == "image":
            media.append(InputMediaPhoto(media=s["url"]))
        elif s["media"] == "video":
            media.append(InputMediaVideo(media=s["url"]))
    
    if media:
        try:
            # Send the media as a group
            await message.reply_media_group(media=media)
            await msg.delete()
        except Exception as e:
            await message.reply_text(f"**Failed to send media: {str(e)}**")
            await msg.delete()
    else:
        await message.reply_text("**No media found in the provided URL.**")
        await msg.delete()

# Start the bot
app.run()
