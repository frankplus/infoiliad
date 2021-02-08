#!/usr/bin/env python
import re
import requests
from bs4 import BeautifulSoup
import datetime

PATTERNS = {
    'nome': r'<div class=\"bold\">(.*)</div>',
    'id': r'ID utente: (\d+.\d+)',
    'numero': r'Numero: (\d+.\d+.\d+)',
    'credito': r'- Credito : <b class="red">(\d.+.(.|,)?)</b>',
    'chiamate': 'Chiamate: <span class="red">(.*)</span><br/>', 
    'sms': r'<div class="conso__text"><span class="red">(\d+) SMS</span>', 
    'mms': r'<span class="red">(\d+) MMS<br/></span>', 
    'dati': '<span class="red">(.*)</span> / (.*)<br/>',
    'data_rinnovo': r'La tua offerta iliad si rinnoverà alle (\d+:\d+) del (\d+\/\d+\/\d+)'
}

def parse_account(html):

    info = dict()
    info["nome"] = re.compile(PATTERNS['nome']).search(str(html)).group(1)
    info["id"] = re.compile(PATTERNS['id']).search(html.text).group(1)
    info["numero"] = re.compile(PATTERNS['numero']).search(html.text).group(1)
    info["credito"] = re.compile(PATTERNS['credito']).search(str(html)).group(1)
    info["data_rinnovo"] = re.compile(PATTERNS['data_rinnovo']).search(str(html)).group(2)

    consumi_italia = dict()
    consumi_estero = dict()

    chiamate = re.findall(re.compile(PATTERNS['chiamate']), str(html))
    consumi_italia['chiamate'] = chiamate[0]
    consumi_estero['chiamate'] = chiamate[1]

    sms = re.findall(re.compile(PATTERNS['sms']), str(html))
    consumi_italia['sms'] = sms[0]
    consumi_estero['sms'] = sms[1]

    mms = re.findall(re.compile(PATTERNS['mms']), str(html))
    consumi_italia['mms'] = mms[0]
    consumi_estero['mms'] = mms[1]

    dati = re.findall(re.compile(PATTERNS['dati']), str(html))
    consumi_italia['dati'] = dati[0][0]
    consumi_italia['totale_dati'] = dati[0][1]
    consumi_estero['dati'] = dati[1][0]
    consumi_estero['totale_dati'] = dati[1][1]

    data = {
        'info': info,
        'consumi_italia': consumi_italia,
        'consumi_estero': consumi_estero
    }

    return data

def get_info(user, password):

    ACCOUNT_URL = "https://www.iliad.it/account/"

    with requests.session() as s:
        # fetch the login page
        s.get(ACCOUNT_URL)
        s.get(ACCOUNT_URL, params={'logout': 'user'})

        # post to the login form
        login_info = {'login-ident': user, 'login-pwd': password}
        response = s.post(ACCOUNT_URL, data=login_info)
        html = BeautifulSoup(response.content, "html.parser")

    if "ID utente o password non corretto." in html.text:
        return None
    else:
        return parse_account(html)

def parse_dati_to_gb(dati):
    if dati == "0b":
        return 0

    gb_regex = re.compile(r'(\d+,\d+)GB')
    match = gb_regex.match(dati)
    if match:
        return float(match.group(1).replace(',', '.'))

    gb_regex = re.compile(r'(\d+)GB')
    match = gb_regex.match(dati)
    if match:
        return float(match.group(1))

    mb_regex = re.compile(r'(\d+,\d+)mb')
    match = mb_regex.match(dati)
    if match:
        return float(match.group(1).replace(',', '.')) / 1024.0



def parse_date(date_str):
    return datetime.datetime.strptime(date_str, '%d/%m/%Y')