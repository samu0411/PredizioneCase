import telegram
import pickle
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import pandas as pd
import sklearn

text = ""
via = ""
sobborgo = ""
numcam = 0
numbagn = 0
numgarage = 0
landarea = 0
floor = 0
build = 0
distcentro = 0
neastn = ""
neastndist = 0
datesold = 0
postcode = 0
latitude = 0
longitude = 0
nearestsch = ""
nearestschdist = 0
nearestschgrade = 0
user_location = 0
dati_inviati = 0
# funzione che gestisce il comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao! Inserisci la tua via e il sobborgo separati da una virgola.")
    context.user_data['dati_inviati'] = 0

# funzione che gestisce i messaggi di testo
def text_message(update, context):
    if  context.user_data['dati_inviati'] == 0:
        text = update.message.text
        via, sobborgo = text.split(',')
        context.user_data['via'] = via.strip()
        context.user_data['sobborgo'] = sobborgo.strip()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Quante camere ha la tua casa?")
        context.user_data['dati_inviati'] += 1
    elif context.user_data['dati_inviati'] == 1:
        numcam = int(update.message.text)
        context.user_data['camere'] = numcam
        context.bot.send_message(chat_id=update.effective_chat.id, text="Quanti bagni ha la tua casa?")
        context.user_data['dati_inviati'] += 1
    elif context.user_data['dati_inviati'] == 2:
        numbagn = int(update.message.text)
        context.user_data['bagni'] = numbagn
        context.bot.send_message(chat_id=update.effective_chat.id, text="Quanti garage ha la tua casa?")
        context.user_data['dati_inviati'] += 1
    elif context.user_data['dati_inviati'] == 3:
        numgarage = update.message.text
        if numgarage.isdigit():
            context.user_data['garage'] = int(numgarage)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Inserisci i mq catastali e quelli calpestabili dell'abitazione")
            context.user_data['dati_inviati'] += 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci un numero intero.")
    elif context.user_data['dati_inviati'] == 4:
        land = update.message.text
        if ',' in land:
            landarea, floor = land.split(',')
            context.user_data['land_area'] = landarea.strip()
            context.user_data['floor_area'] = floor.strip()
            context.bot.send_message(chat_id=update.effective_chat.id, text="Inserire anno di costruzione")
            context.user_data['dati_inviati'] += 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci la virgola troia !.")
    elif context.user_data['dati_inviati'] == 5:
        build = update.message.text
        if build.isdigit():
            context.user_data['anno'] = int(build)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci la distanza dal centro")
            context.user_data['dati_inviati'] += 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Devi inserire un numero intero.")
    elif context.user_data['dati_inviati'] == 6:
        distcentro = update.message.text
        if distcentro.isdigit():
            context.user_data['distanza'] = int(distcentro)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Inserisci il nome e la distanza della stazione più vicina")
            context.user_data['dati_inviati'] += 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Devi inserire un numero intero.")
    elif context.user_data['dati_inviati'] == 7:
        statio = update.message.text
        if ',' in statio:
            neastn, neastndist = statio.split(',')
            context.user_data['nomestazione'] = neastn.strip()
            context.user_data['distanzastazione'] = neastndist.strip()
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Inserisci data dell'ultima vendita della casa")
            context.user_data['dati_inviati'] += 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Non hai inserito la virgola.")
    elif context.user_data['dati_inviati'] == 8:
        datesold = update.message.text
        if datesold.isdigit():
            context.user_data['datavendita'] = int(datesold)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Inserire il codice postale")
            context.user_data['dati_inviati'] += 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Devi inserire un numero intero.")
    elif context.user_data['dati_inviati'] == 9:
        postcode = update.message.text
        if postcode.isdigit():
            context.user_data['codicepostale'] = int(postcode)
            #keyboard = [[InlineKeyboardButton("Invia posizione", request_location=True)]]
            #reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Per favore, invia la tua latitudine.")
            context.user_data['dati_inviati'] += 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Devi inserire un numero intero.")
    elif context.user_data['dati_inviati'] == 10:
        user_location = update.message.text
        context.user_data['latitude'] = int(user_location)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Inserisci la longitudine")
        context.user_data['dati_inviati'] += 1
    elif context.user_data['dati_inviati'] == 11:
        longitude = update.message.text
        context.user_data['longitude'] = int(longitude)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Inserisci il nome e la distanza della scuola più vicina")
        context.user_data['dati_inviati'] += 1
    elif context.user_data['dati_inviati'] == 12:
        scuolaa = update.message.text
        if ',' in scuolaa:
            nearestsch, nearestschdist = scuolaa.split(',')
            context.user_data['nomescuola'] = nearestsch.strip()
            context.user_data['distanzascuola'] = nearestschdist.strip()
            context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci il grado della scuola")
            context.user_data['dati_inviati'] += 1
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Non hai inserito la virgola.")
    elif context.user_data['dati_inviati'] == 13:
        nearestschgrade = update.message.text
        if nearestschgrade.isdigit():
            context.user_data['grado'] = int(nearestschgrade)
            dictionary = {'ADDRESS' : context.user_data['via'],
                          'SUBURB' : context.user_data['sobborgo'],
                          'BEDROOMS' : context.user_data['camere'],
                          'BATHROOMS' : context.user_data['bagni'],
                          'GARAGE' : context.user_data['garage'],
                          'LAND_AREA' : context.user_data['land_area'],
                          'FLOOR_AREA' : context.user_data['floor_area'],
                          'BUILD_YEAR' : context.user_data['anno'],
                          'CBD_DIST' : context.user_data['distanza'],
                          'NEAREST_STN' : context.user_data['nomestazione'],
                          'NEAREST_STN_DIST' : context.user_data['distanzastazione'],
                          'DATE_SOLD' : context.user_data['datavendita'],
                          'POSTCODE': context.user_data['codicepostale'],
                          'LATITUDE': context.user_data['latitude'],
                          'LONGITUDE': context.user_data['longitude'],
                          'NEAREST_SCH': context.user_data['nomescuola'],
                          'NEAREST_SCH_DIST': context.user_data['distanzascuola'],
                          'NEAREST_SCH_RANK': context.user_data['grado']}
            df = pd.DataFrame(dictionary, index=[0])
            df['ADDRESS'] = df['ADDRESS'].astype("category", errors='raise').cat.codes
            df['SUBURB'] = df['SUBURB'].astype("category", errors='raise').cat.codes
            df['NEAREST_STN'] = df['NEAREST_STN'].astype("category", errors='raise').cat.codes
            df['DATE_SOLD'] = df['DATE_SOLD'].astype("category", errors='raise').cat.codes
            df['NEAREST_SCH'] = df['NEAREST_SCH'].astype("category", errors='raise').cat.codes
            context.user_data['dati_inviati'] = 0
            file = open('modello', 'rb')
            modello = pickle.load(file)
            risultato = modello.predict(df)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Il prezzo è" + str(risultato))
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Devi inserire un numero intero.")


# main
if __name__ == '__main__':
    # token del bot
    TOKEN = "6181502382:AAFroZvfszc6PFydtBosUKrEurgyvuSIDek"
    # creazione dell'oggetto bot
    bot = telegram.Bot(TOKEN)

    # creazione dell'updater
    updater = Updater(TOKEN, use_context=True)

    # aggiunta dei gestori di comando e di messaggi di testo
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

    # avvio del bot
    updater.start_polling()
    updater.idle()