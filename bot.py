import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import *
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY,use_context=True)
   
    dp=mybot.dispatcher
    dp.add_handler(CommandHandler('start',start,pass_user_data=True))
    dp.add_handler(CommandHandler('nail',send_nail_design,pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Мои работы)$'),send_nail_design,pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Сменить аватарку)$'),change_avatar,pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    
    dp.add_handler(MessageHandler(Filters.text,talk_to_me,pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()