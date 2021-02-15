import iliad
import json

USER_ID = ""
PASSWORD = ""

login_info = list()
login_info.append([USER_ID, PASSWORD])

iliad.totale_dati_giornalieri(login_info, print_log=True)