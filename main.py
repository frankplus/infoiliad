import api
import json

ID_UTENTE = ""
PASSWORD = ""

info = api.get_info(ID_UTENTE, PASSWORD)
print(json.dumps(info, indent=4))