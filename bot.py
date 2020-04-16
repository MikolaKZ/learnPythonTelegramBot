from glob import glob
from random import choice
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def start(update,context):
    text="Вызван старт"
    logging.info(text)
    update.message.reply_text(text)


def send_nail_design(update,context):
    naiil_list=glob("images/nogt*.jp*g")
    nail_pic=choice(naiil_list) 
    update.message.bot.send_photo(update.message.chat_id,open(nail_pic,'rb'))


def talk_to_me(update,context):
    cur_message=update.message
    userText = "Привет {}! Ты написал: {}".format(cur_message.chat.first_name,cur_message.text)
    update.message.reply_text(userText)


def main():
   mybot = Updater(settings.API_KEY,use_context=True)
   
   dp=mybot.dispatcher
   dp.add_handler(CommandHandler('start',start))
   dp.add_handler(CommandHandler('nail',send_nail_design))

   dp.add_handler(MessageHandler(Filters.text,talk_to_me))
   
   mybot.start_polling()
   logging.info("Бот запущен")
   mybot.idle()


main()


    
