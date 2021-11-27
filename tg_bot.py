from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
from telegram import Update
import sys
from classes import Chats

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


TOKEN = str(sys.argv[1])
chats_ = Chats()


def message(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    chats_.new_chat(chat_id)

    text = chats_.update(chat_id, update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


updater = Updater(token=TOKEN)
dis = updater.dispatcher

message_handler = MessageHandler(Filters.text, message)
dis.add_handler(message_handler)

updater.start_polling()
updater.idle()
