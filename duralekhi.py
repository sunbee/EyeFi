from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import config
import os

repo = os.path.expanduser('~/Desktop/Snaps')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

updater = Updater(token=config.Sanjinator_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="The Sanjinator whishes you a very good day.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=' '.join(word.upper() for word in context.args))

echo_handler = CommandHandler('echo', echo)
dispatcher.add_handler(echo_handler)

def echo_text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text.upper())

message_handler = MessageHandler(Filters.text & (~Filters.command), echo_text)
dispatcher.add_handler(message_handler)

def snap(update, context):
    snap = os.path.join(repo, 'Snap_1.png')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(snap, 'rb'))

snap_handler = CommandHandler('snap', snap)
dispatcher.add_handler(snap_handler)

updater.start_polling()