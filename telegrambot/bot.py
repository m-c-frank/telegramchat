import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
	text = update.message.text
	logging.info(f"Received message: {text}")
	
	# Send message to the Docker container service
	response = requests.post('http://localhost:5000/message', json={'message': text})
	if response.status_code == 200:
		update.message.reply_text('Message sent to server!')
	else:
		update.message.reply_text('Failed to send message to server.')

def main() -> None:
	# Replace with your API token
	token = 'YOUR_TELEGRAM_BOT_API_TOKEN'
	
	# Create Updater and Dispatcher
	updater = Updater(token)
	dispatcher = updater.dispatcher
	
	# Add a handler for text messages
	dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
	
	# Start the bot
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()