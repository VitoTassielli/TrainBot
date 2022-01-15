"""
Created on Sat Nov  9 13:54:00 2019

@author: vitotassielli
"""

import requests
from trenitalia import TrenitaliaBackend
from datetime import datetime

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1024682959:AAEnYoK1QXjAeuafQjzo5CcwDsyDKlWlAmw'
    bot_chatID = '42926019'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

tb = TrenitaliaBackend()

# Ricerca di una stazione (restituisce una lista di risultati)
porta_nuova = tb.search_station(name="torino porta nuova",    # Nome da cercare
                  only_italian=True)           # Cerca solo stazioni italiane (default = False)

bari_centrale = tb.search_station(name="bari centrale",    # Nome da cercare
                  only_italian=True)           # Cerca solo stazioni italiane (default = False)

#print(porta_nuova)
#print(bari_centrale)

#data_partenza = tb._parse_date(string="2019-12-20T17:30:00+01:00")
data_partenza = tb._parse_date(string="2019-12-10T17:30:00+01:00")

# Ricerca di una soluzione di viaggio (restituisce un generatore)
# È possibile inserire data e ora di partenza OPPURE data e ora di arrivo
returnValue = tb.search_solution(origin="830000219",        # ID della stazione di Torino Porta Nuova
                   destination="830011119",                 # ID della stazione di Bari Centrale
                   dep_date=data_partenza,  # Data e ora di partenza
                   arr_date=None,            # Data e ora di arrivo (default = None)
                   adults=1,                 # Numero di adulti (default = 1)
                   children=0,               # Numero di bambini (default = 0)
                   train_type="All",         # Può essere "All", "Frecce", "Regional" (default = "All")
                   max_changes=0,           # Massimo numero di cambi (default = 99)
                   limit=1)                 # Massimo numero di soluzioni da cercare (default = 10)


myTrain = next(returnValue)     #print(myTrain.keys())
dataList = myTrain.get("vehicles", 404)
info = dataList[0] #dict_keys(['dep_date', 'arr_date', 'category', 'number',
                    #          'arr_station', 'dep_station', 'id', 'duration'])
                    

#Estraggo i parametri e mi salvo un log
myDay = 10
myMonth = 12
myYear = 2019                    
                    
#Controllo se stazioni di partenza e arrivo sono corrette
dep_station = info.get("dep_station", 404)
log = str(dep_station)
dep_ID = dep_station.get("id", 404)
dep_name = dep_station.get("name", 404)

arr_station = info.get("arr_station", 404)
log = log + "\n" + str(arr_station)
arr_ID = arr_station.get("id", 404)
arr_name = arr_station.get("name", 404)
 
#Controllo se è InterCityNotte                    
category = info.get("category", 404)
log = log + "\n" + str(category)
isInterCity = category[1]

#Controllo se la data è giusta    
dep_date = info.get("dep_date", 404)
arr_date = info.get("arr_date", 404)
log = log + "\n Partenza:   " + str(dep_date)
log = log + "\n Arrivo:   " + str(arr_date)

if isInterCity == "InterCityNotte" and dep_date.day == myDay and dep_date.month == myMonth and dep_date.year == myYear:
    print(log)

test = telegram_bot_sendtext(log)