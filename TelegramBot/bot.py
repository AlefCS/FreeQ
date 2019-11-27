# -*- coding: utf-8 -*-

import paho.mqtt.client as mqttc
import sys, json
import pytz
import dateutil.parser
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

########################## Command Handlers - BEGIN ############################

##### /start handler #####
def start(update, context):
    start_message = \
    """
Bem vindo ao *FreeQ*, um bot feito para você que não gosta de ficar esperando em filas.

Ficamos felizes que você demonstrou interesse pelo bot.
Lembramos que apesar de o bot já estar rodando a aplicação ainda não está 100% pronta e em pleno funcionamento, então os dados mostrados são "fictícios".

Caso queira checar quantas pessoas estão na fila do RU, basta usar o comando /status\_fila.
    """.strip()
    context.bot.send_message(chat_id=update.message.chat_id, text=start_message, parse_mode=ParseMode.MARKDOWN)

##### /status_fila handler #####
def status_fila(update, context):
    global lastVerification
    local_tz = pytz.timezone("America/Fortaleza")

    rawdate = lastVerification["time"]
    date = rawdate.replace('Z','+00:00')
    date = dateutil.parser.parse(date)
    date = date.replace(tzinfo=pytz.utc).astimezone(local_tz)

    message  = date.strftime(" Às %Hh%M (%d/%m/%Y):\n")
    message += " - Nº de pessoas: *{}*\n".format(lastVerification["value"])
    message += \
    """

_⚠⚠ AVISO ⚠⚠
Lembramos que a aplicação ainda não foi implantada em campo. Então os dados presentes nesta mensagem são fictícios._
    """.strip()

    context.bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode=ParseMode.MARKDOWN)

########################### Command Handlers - END #############################

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, message):
    global lastVerification
    print("Got message on topic '" + str(message.topic) + "'")
    print("Message content:\n" + str(message.payload) + "\n")
    lastVerification = json.loads(message.payload)


broker_url  = "mqtt.tago.io"
broker_port = 8883
dev_token   = "a8891d6c-1794-4759-86e8-8537ee145c00"
topic       = "q/ru/status"

lastVerification = json.loads('{"variable": "init", "value": "-1", "time": "1970-10-10T00:00:00.000Z"}')

client = mqttc.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("", dev_token)
client.tls_set()
client.connect(broker_url, broker_port)

client.subscribe(topic, qos=2)

client.loop_start()

# Get bot Access Token
token_path = sys.path[0] + '/bot_token'
bot_token = open(token_path).read().strip()

# Create updater
updater = Updater(token=bot_token, use_context=True)

# Create handlers (start and example)
start_handler       = CommandHandler('start', start)
status_fila_handler = CommandHandler('status_fila', status_fila)

# Add handlers to dispatcher
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(status_fila_handler)

# Start polling user requests
updater.start_polling()

# Wait for a kill signal to stop Updater
updater.idle()
