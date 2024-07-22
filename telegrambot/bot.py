import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
import dotenv

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('API_KEY')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Replace 'http://localhost:5000/message' with your actual server URL
SERVER_URL = 'http://localhost:5000/message'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response_message = await post_message_to_server(user_message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)

async def post_message_to_server(message: str):
    try:
        response = requests.post(SERVER_URL, json={'message': message})
        if response.status_code == 200:
            return 'Message posted successfully.'
        else:
            return f'Failed to post message. Status code: {response.status_code}'
    except requests.RequestException as e:
        return f'An error occurred: {e}'

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(unknown_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
