from utilits import get_keyboard
from glob import glob
from random import choice
from emoji import emojize
from telegram import ParseMode
from telegram.ext import messagequeue as mq

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from bot import subsctibers
from db import db, get_or_create_user
import logging
import settings

def user_subscribe(update,context):
    context.user_data=get_or_create_user(db,update.effective_user,update.message)
    print(user)
    subsctibers.add(update.message.chat_id)
    update.message.reply_text("Вы подписались, наберите /unsubscribe чтобы отписаться")

def user_unsubscribe(update,context):
    if update.message.chat_id in subsctibers:
        subsctibers.remove(update.message.chat_id)
        update.message.reply_text("Вы отписались, спасибо что были с нами")
    else:
        update.message.reply_text("Вы не подписаны, наберите /subscribe, что бы подписаться")



def start(update,context):
    
    emo=emojize(choice(settings.USER_EMOJI),use_aliases=True)
    greatEmo=emojize(choice(settings.GREAT_EMOJI),use_aliases=True)
    context.user_data["emo"]=greatEmo
    chatInfo=getChatInfo(update)
    
    text="Привет {}! Меня зовут мастер Биба!{}".format(chatInfo.first_name,greatEmo)
    update.message.reply_text(text,reply_markup=get_keyboard())

def getChatInfo(update):
    return update.message.chat

def anketa_start(update,context):
    update.message.reply_text("Как вас зовут? Напишите Имя и Фамилию", 
                                reply_markup=ReplyKeyboardRemove())
    return "name"

def anketa_get_name(update, context):
    user_name = update.message.text
    if len(user_name.split(" "))!=2:
        update.message.reply_text("Пожалуйста введите имя и фамилию через пробел")
        return "name"
    else:
        context.user_data['anketa_name'] = user_name
        reply_keyboard=[
                            ["1","2","3","4","5"]
                        ]
        update.message.reply_text("Оцените работу мастера по 5 бальной шкале",reply_markup=ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True))
        return "scors"

def anketa_scor(update, context):
    context.user_data['anketa_scors']=update.message.text
    update.message.reply_text("""Пожалуйста напишите отзыв в свободной форме 
                                или /cancel чтобы пропустить этот шаг""")
    return "comment"

def anketa_comment(update, context):
    context.user_data['anketa_comment']=update.message.text
    text="""
    <b>Фамилия Имя:</b>{anketa_name}
    <b>Оценка:</b>{anketa_scors}
    <b>Комментарий:</b>{anketa_comment}""".format(**context.user_data)
    
    update.message.reply_text(text,reply_markup=get_keyboard(),parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def anketa_cancel_comment(update, context):
    context.user_data['anketa_comment']=update.message.text
    text="""
    <b>Фамилия Имя:</b>{anketa_name}
    <b>Оценка:</b>{anketa_raiting}""".format(**context.user_data)
    update.message.reply_text(text,reply_markup=get_keyboard(),parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def anketa_dontknow(update, context):
    update.message.reply_text("Не понимаю")

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

def my_test(update,context):
    for subscriber in subsctibers:
        #context.bot.sendMessage(chat_id=subscriber,text="text test spam")
        for ix in range(10):
            context.bot.send_message(chat_id=subscriber,text="text test spam")
            #context.bot.sendMessage(chat_id=subscriber,text="Пока!")
            #context.job.schedule_removal()

def set_alarm(update,context):
    try:
        seconds = abs(int(context.args[0]))
        context.bot.send_message(chat_id=update.message.chat_id,
                             text='Установлен будильник на {} секунд!'.format(seconds))
        context.job_queue.run_once(alarm,seconds,context=update.message.chat_id)
    except (IndexError, ValueError):
        update.message.reply_text("Введите число секунд после команды /alarm")

def alarm(context):
    context.bot.sendMessage(chat_id=context.job.context,text="Сработал будильник!")