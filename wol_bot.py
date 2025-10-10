#!/usr/bin/env python3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from wakeonlan import send_magic_packet
from ping3 import ping
import asyncio
from config import BOT_TOKEN, TARGET_IP, TARGET_MAC, USER_ID

async def check_machine_status(context, chat_id):
    await context.bot.send_message(chat_id, f"Trying to wake up {TARGET_IP}...")
    if ping(TARGET_IP, timeout=2):
        await is_online(chat_id, context)
        return True

async def wol_command(update, context):
    if update.effective_user.id != USER_ID:
        return
    attempts = 60
    for _ in range(attempts):
        try:
            res = await check_machine_status(context, update.effective_chat.id)
            if res:
                return True
            send_magic_packet(TARGET_MAC)
        except Exception as e:
            await update.message.reply_text(f"Error sending WOL packet:\n{str(e)}")
            return
        await asyncio.sleep(5)

    await context.bot.send_message(
        chat_id=USER_ID,
        text="Could not power on the machine"
    )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != USER_ID:
        return
    await context.bot.send_message(
        USER_ID,
        "🤖 Wake-on-LAN Bot Ready!\n\n"
        "Commands:\n"
        "/wol - Wake up the target machine\n"
        "/status - Check if machine is online"
    )

async def is_online(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    if ping(TARGET_IP, timeout=2):
        await context.bot.send_message(chat_id, "🟢 Machine is online")

def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handler for /wol
    application.add_handler(CommandHandler("start", start_command))
    # application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("wol", wol_command))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
