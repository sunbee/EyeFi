from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import config
import os
 
if os.environ.get('BOT'):
    repo = "/app/snaps"
    BOT = os.environ.get('BOT')
else:
    repo = os.path.expanduser('~/Desktop/Snaps')
    BOT = "Sanjinator"

token = config.TeleTokens.get(BOT)
    

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"The {BOT} whishes you a very good day.")

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

def alert(update, context):
    """
    Use: snap_alert = max(glob.glob(os.path.join(repo, '*.jpeg')), key=os.path.getctime)
    """
    snaps = glob.glob(os.path.join(repo, '*.jpeg'))
    if len(snaps) > 0:
        snap_alert = max(snaps, key=os.path.getctime)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(snap_alert, 'rb'))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing to see here.")

updater.start_polling()