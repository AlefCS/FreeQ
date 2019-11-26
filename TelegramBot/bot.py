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
Bem vindo ao *FreeQ*!

Ficamos felizes que você demonstrou interesse pelo bot. Infelizmente o mesmo ainda está sendo construído e não se encontra em pleno funcionamento.

Caso queira ter um exemplo de como o FreeQ irá funcionar, basta usar o comando /example.
    """
    start_message = start_message[1:-2]
    context.bot.send_message(chat_id=update.message.chat_id, text=start_message, parse_mode=ParseMode.MARKDOWN)

##### /example handler #####
def example(update, context):
    example_message = \
    """
Às 12h05 (26/09/2019):
    - Nº de pessoas: *16*
    - Tempo de espera: *7 minutos*

_⚠⚠ AVISO ⚠⚠
Lembramos que esta mensagem trata-se apenas de um exemplo e os dados nela apresentados são fictícios._
    """
    example_message = example_message[1:-2]
    context.bot.send_message(chat_id=update.message.chat_id, text=example_message, parse_mode=ParseMode.MARKDOWN)

def verificarSituacao(update, context):
    global lastVerification
    local_tz = pytz.timezone("America/Fortaleza")

    rawdate = lastVerification["time"]
    date = rawdate.replace('Z','+00:00')
    date = dateutil.parser.parse(date)
    date = date.replace(tzinfo=pytz.utc).astimezone(local_tz)

    message  = " Às {}:\n".format(date)
    message += " - Nº de pessoas: *{}*\n".format(lastVerification["value"])

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
bot_token = open(token_path).read()[0:-1]

# Create updater
updater = Updater(token=bot_token, use_context=True)

# Create handlers (start and example)
start_handler     = CommandHandler('start', start)
example_handler   = CommandHandler('example', example)
verificarSituacao_handler = CommandHandler('verificarSituacao', verificarSituacao)

# Add handlers to dispatcher
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(example_handler)
updater.dispatcher.add_handler(verificarSituacao_handler)

# Start polling user requests
updater.start_polling()

# Wait for a kill signal to stop Updater
updater.idle()
