from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
import logging
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def start(update,context):
    text="Вызван старт"
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(update,context):
    cur_message=update.message
    userText = "Привет {}! Ты написал: {}".format(cur_message.chat.first_name,cur_message.text)
    print(update.message)
    update.message.reply_text(userText)


def main():
   mybot = Updater(settings.API_KEY,use_context=True)
   
   dp=mybot.dispatcher
   dp.add_handler(CommandHandler('start',start))
   dp.add_handler(MessageHandler(Filters.text,talk_to_me))
   
   mybot.start_polling()
   logging.info("Бот запущен")
   mybot.idle()


main()


    
