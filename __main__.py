from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from config import token
from random import randint
from redchaucha import *
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def mensajes(bot, update, args):
    try:
        user = update.message.from_user
        addr = getaddress(user.id)[0]

        max_read = int(args[0])

        if max_read > 0:
            msg = getTx(addr, max_read)

        if len(msg) == 0:
            msg = 'No tienes mensajes en el blockchain'
    except:
        msg = "Error >:C\nIntenta más tarde...\n\n"
        msg += "Modo de uso: /mensajes cantidad"

    logger.info("mensajes(%i) => %s" % (user.id, msg))
    update.message.reply_text("%s" % msg, parse_mode=ParseMode.MARKDOWN)

def op_return(bot, update, args):
    try:
        user = update.message.from_user
        info = getaddress(user.id)
        op_return = ' '.join(args)

        if len(op_return) > 0:
            msg = sendTx(info, 0.001, info[0], op_return)
        else:
            msg = "No hay mensaje, no puedo hacer nada :C"
    except:
        msg = "Error >:C\nIntenta más tarde..."

    logger.info("op_return(%i) => %s" % (user.id, msg))
    update.message.reply_text("%s" % msg)

def start(bot, update):
    msg =  "*Holi !*"
    logger.info("start() => %s" % (msg))
    update.message.reply_text("%s" % msg, parse_mode=ParseMode.MARKDOWN)

def qr(bot, update):
    user = update.message.from_user
    info = getaddress(user.id)

    logger.info("qr(%i) => %s" % (user.id, info[0]))
    update.message.reply_photo(photo='https://api.qrserver.com/v1/create-qr-code/?size=300x300&margin=2&data=' + info[0])

def sendall(bot, update, args):
    try:
        user = update.message.from_user
        info = getaddress(user.id)

        max_amount = getbalance(info[0])[0]
        receptor = args[0]

        msg = sendTx(info, max_amount, receptor, 'Quirquincho sendall')

    except:
        msg = "Error >:C\nIntenta más tarde...\n\n"
        msg += "Modo de uso: /sendall address"

    logger.info("sendall(%i) => %s" % (user.id, msg))
    update.message.reply_text("%s" % msg)

def send(bot, update, args):
    try:
        user = update.message.from_user
        info = getaddress(user.id)

        amount = float(args[0])
        receptor = args[1]

        msg = sendTx(info, amount, receptor, 'Quirquincho')

    except:
        msg = "Error >:C\nIntenta más tarde...\n\n"
        msg += "Modo de uso: /send monto address"

    logger.info("send(%i) => %s" % (user.id, msg))
    update.message.reply_text("%s" % msg)


def balance(bot, update):
    try:
        # Descubrimiento de address
        user = update.message.from_user

        addr = getaddress(user.id)[0]
        balance = getbalance(addr)

        total = balance[0] + balance[2]

        # MSG
        msg = "Tienes %f CHA en tu dirección\n"
        msg += "%f CHA para utilizar y %f CHA sin confirmar.\n\n"
        msg += "Tu address es %s"

        msg = msg % (total, balance[0], balance[2], addr)
    except:
        msg = "No se pudo ejecutar la lectura de balance :C"

    logger.info("balance(%i) => %s" % (user.id, msg.replace('\n', '')))
    update.message.reply_text("%s" % msg)

def azar(bot, update, args):
    try:
        max_number = int(args[0])
        rand_number = randint(0, max_number)

        msg = "Número al azar (0, %s): %s\n" % (max_number, rand_number)
    except:
        msg = "Error >:C\n\n"
        msg += "Modo de uso: /azar [N]"

    logger.info("random(%i) => %s" % (update.message.from_user.id, msg))
    update.message.reply_text("%s" % msg)

def error(bot, update, error):
    logger.warning('Update: "%s" - Error: "%s"' % (update, error))

# Main loop
def main():
    global quirquincho

    # Configuración
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Listado de comandos
    dp.add_handler(CommandHandler("qr", qr))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("mensajes", mensajes, pass_args=True))
    dp.add_handler(CommandHandler("op_return", op_return, pass_args=True))
    dp.add_handler(CommandHandler("send", send, pass_args=True))
    dp.add_handler(CommandHandler("sendall", sendall, pass_args=True))
    dp.add_handler(CommandHandler("azar", azar, pass_args=True))

    # log all errors
    dp.add_error_handler(error)

    quirquincho = getaddress('Quirquincho')
    # Inicio de bot
    logger.info("Quirquincho V 2.0 - %s" % quirquincho[0])
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
