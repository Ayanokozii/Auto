import os
import sys
import time
import asyncio
import logging
import datetime

from config import Config
from helper.database import db
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyromod.exceptions import ListenerTimeout

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize user client
user = Client(
    name="User",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.SESSION
)

# Command to get bot status and statistics
@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))
    start_time = time.time()
    st = await message.reply('**Accessing Details...**')
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    await st.edit(
        text=f"**--Bot Status--** \n\n"
             f"**⌚️ Bot Uptime:** {uptime} \n"
             f"**🐌 Current Ping:** `{time_taken_ms:.3f} ms` \n"
             f"**👭 Total Users:** `{total_users}`"
    )

# Command to restart the bot
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(bot, message):
    await message.reply_text("🔄 Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Command to broadcast a message to all users
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot, message):
    await bot.send_message(Config.LOG_CHANNEL, f"{message.from_user.mention} or {message.from_user.id} has started the broadcast.")
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    sts_msg = await message.reply_text("Broadcast Started...")
    done, success, failed = 0, 0, 0
    start_time = time.time()
    total_users = await db.total_users_count()
    
    for user in all_users:
        sts = await send_msg(user['id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
        done += 1
        if not done % 20:
            await sts_msg.edit(
                f"Broadcast in Progress: \n"
                f"Total Users: {total_users} \n"
                f"Completed: {done} / {total_users}\n"
                f"Success: {success}\n"
                f"Failed: {failed}"
            )
    
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(
        f"Broadcast Completed: \n"
        f"Completed in: `{completed_in}`.\n\n"
        f"Total Users: {total_users}\n"
        f"Completed: {done} / {total_users}\n"
        f"Success: {success}\n"
        f"Failed: {failed}"
    )

async def send_msg(user_id, message):
    try:
        await message.forward(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        logger.info(f"{user_id} : Deactivated/Blocked/Invalid ID")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500

# Command to accept all pending requests
@Client.on_message(filters.private & filters.command('acceptall') & filters.user(Config.ADMIN))
async def handle_acceptall(bot, message):
    ms = await message.reply_text("**Please Wait...**")
    chat_ids = await db.get_channel(Config.ADMIN)
    
    if not chat_ids:
        return await ms.edit("**I'm not admin in any Channel or Group yet!**")

    button = [[InlineKeyboardButton(f"{(await bot.get_chat(id)).title} {str((await bot.get_chat(id)).type).split('.')[1]}", callback_data=f'acceptallchat_{id}')] for id in chat_ids]
    await ms.edit(
        "Select Channel or Group Below Where you want to accept pending request\n\n"
        "Below Channels or Groups I'm Admin in:",
        reply_markup=InlineKeyboardMarkup(button)
    )

# Command to decline all pending requests
@Client.on_message(filters.private & filters.command('declineall') & filters.user(Config.ADMIN))
async def handle_declineall(bot, message):
    ms = await message.reply_text("**Please Wait...**")
    chat_ids = await db.get_channel(Config.ADMIN)
    
    if not chat_ids:
        return await ms.edit("**I'm not admin in any Channel or Group yet!**")

    button = [[InlineKeyboardButton(f"{(await bot.get_chat(id)).title} {str((await bot.get_chat(id)).type).split('.')[1]}", callback_data=f'declineallchat_{id}')] for id in chat_ids]
    await ms.edit(
        "Select Channel or Group Below Where you want to decline pending requests\n\n"
        "Below Channels or Groups I'm Admin in:",
        reply_markup=InlineKeyboardMarkup(button)
    )

# Callback to accept all pending requests in a specific chat
@Client.on_callback_query(filters.regex('^acceptallchat_'))
async def handle_accept_pending_request(bot, update: CallbackQuery):
    chat_id = update.data.split('_')[1]
    ms = await update.message.edit("**Please Wait Accepting the pending requests... ♻️**")
    try:
        while True:
            try:
                await user.approve_all_chat_join_requests(chat_id=chat_id)
            except FloodWait as t:
                await asyncio.sleep(t.value)
                await user.approve_all_chat_join_requests(chat_id=chat_id)
            except Exception as e:
                logger.error(f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(e).__name__} - {e}")
    except:
        await update.message.reply_text(f"**Task Completed** ✓ **Approved ✅ All Pending Join Requests**")
        await ms.delete()

# Callback to decline all pending requests in a specific chat
@Client.on_callback_query(filters.regex('^declineallchat_'))
async def handle_decline_pending_request(bot, update: CallbackQuery):
    chat_id = update.data.split('_')[1]
    ms = await update.message.edit("**Please Wait Declining all the pending requests... ♻️**")
    try:
        while True:
            try:
                await user.decline_all_chat_join_requests(chat_id=chat_id)
            except FloodWait as t:
                await asyncio.sleep(t.value)
                await user.decline_all_chat_join_requests(chat_id=chat_id)
            except Exception as e:
                logger.error(f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(e).__name__} - {e}")
    except:
        await ms.delete()
        await update.message.reply_text("**Task Completed** ✓ **Declined ❌ All The Pending Join Requests**")

# Start the client
user.run()
