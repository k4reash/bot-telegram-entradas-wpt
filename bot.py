#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
WPT BOT
"""
import schedule
import logging
import os
import time
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# This list stores all the users that use the bot.
user_id = []

token = "Insert your API token"
enviado = 0
palabra = "Alicante"

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Bienvenido, te avisaré cuando haya entradas para la prueba WPT Alicante \nUtiliza /help para obtener más información.')
    uid = update.message.chat_id
    add_user(uid)

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Utiliza /entradas para obtener las entradas actuales. \nUtiliza /stop para detener el bot.')

def echo(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Comando no válido. !\nUtiliza /help para obtener los comandos disponibles.')

def stop(update, context):
    """Stop alerts"""
    update.message.reply_text('Ya no te avisaré más de próximos cambios.')
    uid = update.message.chat_id
    delete_user(uid)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# ==================== ADMIN FUNCTIONS =========================================

def cambiar_entradas(update, context):
    """Cambiar entrada a buscar"""
    global palabra
    global enviado
    z = update.message.text
    x = z.replace("/nuevabusqueda","")
    palabra = x.replace(" ","")
    print(palabra)
    enviado = 0
    update.message.reply_text('Perfecto, te avisaré cuando haya entradas disponibles para: ' +palabra)

def busqueda_actual(update, context):
    """Indica para que campeonato está buscando entradas actualmente."""
    global palabra
    update.message.reply_text('Actualmente estoy buscando entradas nuevas para: '+palabra)

# ==================== OTHER FUNCTIONS =========================================

def add_user(uid):
    """Adds a user to the user database if not there."""

    if uid not in user_id:
        user_id.append(uid)

def delete_user(uid):
    """Delete a user to the user database if not there."""

    if uid in user_id:
        user_id.remove(uid)

def entradas(update, context):
    """Funcion que devuelve el scrapeo al usuario."""

    message = get_scrapeo()
    update.message.reply_text(message)

def broadcast(message):
    """Enviar el scrapeo a todos."""

    bot = telegram.Bot(token=token)
    for uid in user_id:
        bot.sendMessage(chat_id=uid, text=message)

def get_scrapeo():
    """Leemos el fichero que contiene el scrapeo."""

    r_file = open("kk.txt", "r")
    message = r_file.readline() + "\n"
    r_file.close()

    return message

def job():
    """Funcion que ejecuta la comprobacion de cambio de entradas"""

    os.system("python web-s.py")
    print("Ejecutado scrapeo.")

    r_file = open("kk.txt", "r")
    texto = r_file.readline() + "\n"
    r_file.close()

    global palabra
    global enviado

    if palabra in texto and enviado != 1:
        broadcast("¡¡¡Ya estan las nuevas entradas!!! \nhttps://www.worldpadeltour.com/entradas")
        print("Datos enviados.")
        enviado = 1
    else:
        print("No existe")

def sendToUser():
    """	Send a mensage to a telegram user specified on chatId chat_id must be a number!	"""

    bot = telegram.Bot(token=token)
    for uid in user_id:
        bot.sendMessage(chat_id=uid, text="hola")	        

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("entradas", entradas))
    dp.add_handler(CommandHandler("stop", stop))

    # comandos admin

    dp.add_handler(CommandHandler("nuevabusqueda", cambiar_entradas))
    dp.add_handler(CommandHandler("busqueda", busqueda_actual))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    
    # Declaration of the schedule
    schedule.every(5).seconds.do(job)

    while True:
        schedule.run_pending()
        # The sleep prevents the CPU to work unnecessarily.
        time.sleep(1)


if __name__ == '__main__':
    main()
