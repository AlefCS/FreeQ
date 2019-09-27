from telegram import ParseMode
from telegram.ext import Updater, CommandHandler

########################## Command Handlers - BEGIN ############################

##### /start handler #####
def start(update, context):
	start_message = \
	"""
Bem vindo ao *FreeQ*!

Ficamos felizes que você demonstrou interesse pelo bot. Infelizmente o mesmo ainda está sendo contruído e não se encontra em pleno funcinamento.

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
########################### Command Handlers - END #############################

# Get bot Access Token
bot_token = open('bot_token').read()[0:-1]

# Create updater
updater = Updater(token=bot_token, use_context=True)

# Create handlers (start and example)
start_handler   = CommandHandler('start', start)
example_handler = CommandHandler('example', example)

# Add handlers to dispatcher
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(example_handler)

# Start polling user requests
updater.start_polling()

# Wait for a kill signal to stop Updater
updater.idle()
