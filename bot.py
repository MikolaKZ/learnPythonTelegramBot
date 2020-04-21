from emoji import emojize
from glob import glob
from random import choice
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def start(update,context):
    
    emo=emojize(choice(settings.USER_EMOJI),use_aliases=True)
    greatEmo=emojize(choice(settings.GREAT_EMOJI),use_aliases=True)
    context.user_data["emo"]=greatEmo
    chatInfo=getChatInfo(update)
    
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)


    text="Привет {}! Меня зовут мастер Биба!{}".format(chatInfo.first_name,greatEmo)

    my_keyboard=ReplyKeyboardMarkup([
                                        ['Мои работы','Сменить аватарку'],
                                        [contact_button,location_button]
                                    ])
    update.message.reply_text(text,reply_markup=my_keyboard)

def getChatInfo(update):
    return update.message.chat

def send_nail_design(update,context):
    naiil_list=glob("images/nogt*.jp*g")
    nail_pic=choice(naiil_list) 
    update.message.bot.send_photo(update.message.chat_id,open(nail_pic,'rb'))


def talk_to_me(update,context):
    cur_message=update.message
    userText = "{}Привет {}! Ты написал: {}".format(context.user_data.get("emo"),cur_message.chat.first_name,cur_message.text)
    update.message.reply_text(userText)


def get_contact(update,context):
    print (update.message.contact)


def change_avatar(update,context):
    greatEmoOld = None
    if 'emo' in context.user_data:
        greatEmoOld = context.user_data['emo']
        del context.user_data['emo']
    greatEmo=emojize(choice(settings.GREAT_EMOJI),use_aliases=True)
    context.user_data["emo"]=greatEmo
    if greatEmoOld is None:
        update.message.reply_text("New avatar added = {}".format(greatEmo))
    else:
        update.message.reply_text("Avatar has been changed from {} to {}".format(greatEmoOld,greatEmo))
    

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



main()
    


