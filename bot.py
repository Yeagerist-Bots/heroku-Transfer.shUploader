from telethon import TelegramClient, events, Button
from telethon.tl.functions.users import GetFullUserRequest
from download_from_url import download_file, get_size
from file_handler import send_to_transfersh_async, progress
import os
import time
import datetime
import aiohttp
import asyncio

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token =os.environ.get("BOT_TOKEN")
                          
download_path = "Downloads/"

bot = TelegramClient('Uploader bot', api_id, api_hash).start(bot_token=bot_token)

BUTTONS = [
  [Button.url("📢 Bot Updates", url="https://t.me/AsmSafone"), 
   Button.url("👥 Support", url="https://t.me/Safothebot")], 
  [Button.url("🤖 Developer", url="https://t.me/AmiFutami"), 
   Button.url("👨🏻‍💻 Source Code", url="https://github.com/Achu2234/heroku-Transfer.shUploader")]]

START_MSG = "**Hii {mention}, I'm a transfer.sh Uploader Bot\n\nSend any file or direct download link to upload and get the transfer.sh download link \n\n🤖 Bot Made by [Achu Biju](https://t.me/AmiFutami)**" 

@bot.on(events.NewMessage(incoming=True, pattern="/start", func = lambda e: e.is_private))
async def start(event):
    """Send a message when the command /start is issued."""
    new = await bot(GetFullUserRequest(event.sender_id))
    check = await check_user(event.sender_id)
    if not is_added(event.sender_id):
        add_user(event.sender_id)
    if check is True:
        await event.reply(START_MSG.format(mention=new.user.first_name),
                        buttons=BUTTONS)
    else:
        await event.reply("**{} You need to join my channel to use me!**".format(new.user.first_name), 
                          buttons=[Button.url("📢 Join My Updates Channel", url="https://t.me/AsmSafone")])

@bot.on(events.NewMessage)
async def echo(update):
    """Echo the user message."""
    msg = await update.respond("**Processing...**")
    
    try:
        if not os.path.isdir(download_path):
            os.mkdir(download_path)
            
        start = time.time()
        
        if not update.message.message.startswith("/") and not update.message.message.startswith("http") and update.message.media:
            await msg.edit("**Downloading start...**")
            file_path = await bot.download_media(update.message, download_path, progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, msg, start)))
        else:
            url = update.text
            filename = os.path.join(download_path, os.path.basename(url))
            file_path = await download_file(update.text, filename, msg, start, bot)
            
        print(f"file downloaded to {file_path}")
        try:
            await msg.edit("Download finish!\n\n**Now uploading...**")
            download_link, final_date, size = await send_to_transfersh_async(file_path, msg)
            name = os.path.basename(file_path)
            await msg.edit(f"**Name: **`{name}`\n**Size:** `{size}`\n**Link:** {download_link}")
        except Exception as e:
            print(e)
            await msg.edit(f"Uploading Failed\n\n**Error:** {e}")
        finally:
            os.remove(file_path)
            print("Deleted file :", file_path)
    except Exception as e:
        print(e)
        await msg.edit(f"Download link is invalid or not accessable\n\n**Error:** {e}")

def main():
    """Start the bot."""
    print("\nBot started...\n")
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
