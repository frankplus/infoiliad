import api
import json
import datetime

ID_UTENTE = ""
PASSWORD = ""

all_accounts = list()
all_accounts.append(api.get_info(ID_UTENTE, PASSWORD))


print(json.dumps(all_accounts, indent=4))

totale_dati_giornalieri = 0

for account in all_accounts:
    consumo = api.parse_dati_to_gb(account["consumi_italia"]["dati"])
    totale = api.parse_dati_to_gb(account["consumi_italia"]["totale_dati"])
    rimanenti = totale - consumo
    data_rinnovo = api.parse_date(account["info"]["data_rinnovo"])
    giorni_rimanenti = (data_rinnovo - datetime.datetime.now()).days + 1
    dati_rimanenti_giornalieri = rimanenti / giorni_rimanenti
    totale_dati_giornalieri += dati_rimanenti_giornalieri

    print(account["info"]["numero"])
    print("rimanenti: " + str(rimanenti))
    print("giorni_rimanenti: " + str(giorni_rimanenti))
    print()

print("totale_dati_giornalieri: " + str(totale_dati_giornalieri))