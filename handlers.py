from utilits import get_keyboard
from glob import glob
from random import choice
from emoji import emojize
import logging
import settings

def start(update,context):
    
    emo=emojize(choice(settings.USER_EMOJI),use_aliases=True)
    greatEmo=emojize(choice(settings.GREAT_EMOJI),use_aliases=True)
    context.user_data["emo"]=greatEmo
    chatInfo=getChatInfo(update)
    
    text="Привет {}! Меня зовут мастер Биба!{}".format(chatInfo.first_name,greatEmo)

    update.message.reply_text(text,reply_markup=get_keyboard())

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