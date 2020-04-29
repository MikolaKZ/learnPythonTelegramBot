import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from handlers import *
import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

subsctibers = set()                   

def main():

    

    mybot = Updater(settings.API_KEY,use_context=True)
   
    dp=mybot.dispatcher

    mybot.job_queue.run_repeating(my_test,interval=5)

    anketa = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Заполить анкету)$'),anketa_start,pass_user_data=True)],
        states={
                "name":  [MessageHandler(Filters.text,anketa_get_name,pass_user_data=True)],    
                "scors": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_scor, pass_user_data=True)],
                "comment": [MessageHandler(Filters.text, anketa_comment, pass_user_data=True),
                            CommandHandler("cancel",anketa_cancel_comment, pass_user_data=True)]
                },
        fallbacks=[MessageHandler(Filters.text, anketa_dontknow, pass_user_data=True)])
   
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('start',start,pass_user_data=True))
    dp.add_handler(CommandHandler("subscribe",user_subscribe))
    dp.add_handler(CommandHandler("unsubscribe",user_unsubscribe))
    dp.add_handler(CommandHandler('nail',send_nail_design,pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Мои работы)$'),send_nail_design,pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Сменить аватарку)$'),change_avatar,pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    
    

    dp.add_handler(MessageHandler(Filters.text,talk_to_me,pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()