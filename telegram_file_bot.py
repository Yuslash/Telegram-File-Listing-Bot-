import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Telegram bot token
TELEGRAM_BOT_TOKEN = 'YOUR_TELEGRAM_TOKEN'

# Directory path where files are located
FILES_DIRECTORY = 'D:\\PATH\\To\\FIle'

# Initialize the Telegram Bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Function to send a message indicating bot connection

def send_connection_message(chat_id):
    bot.send_message(chat_id=chat_id, text='Bot connected and ready to use!')

# Function to list files in the directory and send the count


def list_files_and_send_count(chat_id):
    files = [f for f in os.listdir(FILES_DIRECTORY)]
    num_files = len(files)
    if num_files > 0:
        keyboard = InlineKeyboardMarkup()
        for file_name in files:
            keyboard.row(InlineKeyboardButton(
                text=file_name, callback_data=file_name))
        bot.send_message(
            chat_id=chat_id, text=f'There are {num_files} files available.', reply_markup=keyboard)
    else:
        bot.send_message(chat_id=chat_id, text='No files available.')

# Handler for the /start command


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    send_connection_message(chat_id)
    list_files_and_send_count(chat_id)

# Handler for callback queries from inline keyboard


@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    file_name = call.data
    file_path = os.path.join(FILES_DIRECTORY, file_name)
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as file:
                bot.send_document(chat_id=call.message.chat.id, document=file)
        except Exception as e:
            bot.send_message(chat_id=call.message.chat.id,
                             text=f'Error: {str(e)}')
    else:
        bot.send_message(chat_id=call.message.chat.id,
                         text='File not found. Please select a valid file.')



@bot.message_handler(commands=['list'])
def handle_list(message):
    chat_id = message.chat.id
    list_files_and_send_count(chat_id)

# Handler for the /help command


@bot.message_handler(commands=['help'])
def handle_help(message):
    chat_id = message.chat.id
    help_message = (
        "Welcome to the Bot Help!\n\n"
        "Available Commands:\n"
        "/start - Start the bot and view available files.\n"
        "/list - List all available files.\n"
        "/help - Display this help message.\n"
    )
    bot.send_message(chat_id=chat_id, text=help_message)


# Start the bot
bot.polling()
