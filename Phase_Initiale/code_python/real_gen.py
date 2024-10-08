#!/usr/bin/env python

import xmltodict  # type: ignore
import datetime
import xmlschema  # type: ignore
from pprint import pprint
from datetime import datetime, timezone
from faker import Faker
import random
import copy

SCHEMA_PAC8 = '../doc_xsd/pacs.008.001.07.xsd'

pac9_xsd = xmlschema.XMLSchema(SCHEMA_PAC8)


# pour avoir une séquence variable

class MsgIdSeq:
    def __init__(self) -> None:
        self._seq = 0

    def gen(self):
        self._seq += 1

        return self._seq


template = {'Document': {'@xmlns': 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.07',
                         '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                         'FIToFICstmrCdtTrf': {'GrpHdr': {'MsgId': None,
                                                          'CreDtTm': None,
                                                          'NbOfTxs': None,
                                                          'TtlIntrBkSttlmAmt': {'@Ccy': 'MRU',
                                                                                '$': None},
                                                          'IntrBkSttlmDt': None,
                                                          'SttlmInf': {'SttlmMtd': 'CLRG',
                                                                       'ClrSys': {'Prtry': 'ACH'}},
                                                          'InstgAgt': {'FinInstnId': {'BICFI': None}}},
                                               'CdtTrfTxInf': [None]
                                               }
                         }
            }

credit_template = {'PmtId': {'InstrId': '',
                             'EndToEndId': '',
                             'TxId': ''},
                   'PmtTpInf': {'SvcLvl': {'Cd': 'SEPA'},
                                'LclInstrm': {'Cd': 'B2B'},
                                'CtgyPurp': {'Cd': 'CASH'}},
                   'IntrBkSttlmAmt': {'@Ccy': 'MRU',
                                      '$': None},
                   'ChrgBr': 'SLEV',
                   'Dbtr': {'Nm': None},
                   'DbtrAcct': {'Id': {'Othr': {'Id': None}}},
                   'DbtrAgt': {'FinInstnId': {'BICFI': None}},
                   'CdtrAgt': {'FinInstnId': {'BICFI': 'BCEMMRMR'}},
                   'Cdtr': {'Nm': None},
                   'CdtrAcct': {'Id': {'Othr': {'Id': None}}},
                   'Purp': {'Cd': 'ADVA'},
                   'RmtInf': {'Ustrd': None}}


# recuperer les bic des banks
def banks_data(banks_path):
    banks_data = {}
    with open(banks_path, 'r') as f:
        # Lire et l'ignorer  la première ligne qui contient (bic name)
        header = f.readline()

        # passons au reste du fichier en passant ligne par ligne
        for line in f:
            bic, name = line.strip().split('\t')
            banks_data[name] = bic

    return banks_data


def lire_Cdtr(fichier):
    Cdtr = {}
    with open(fichier, 'r', encoding='utf-8') as f:
        # Lire et ignorer la première ligne (en-tête)
        en_tete = f.readline()

        # Parcourir le reste du fichier ligne par ligne
        for ligne in f:
            # Séparer les éléments de la ligne par tabulation
            elements = ligne.strip().split('\t')
            # Assigner les valeurs aux variables
            nom, numero_compte = elements[2], elements[1]

            # Ajouter au dictionnaire
            Cdtr[nom] = numero_compte
            # Cdtr[nom] = list(ligne[0], ligne[1], ligne[4], ligne[5])
            

    return Cdtr


# initialiser un objet de la classe MsgIdSeq
msg_id_seq = MsgIdSeq()
tx_id_seq = MsgIdSeq()

# dictionnaire dont les clés sont les noms des banques et les valuers leurs bic
banks_path = '../dat/banks.tsv'
bank_data = banks_data(banks_path)
banks_names = list(bank_data.keys())

# dictionnaire dont les clés sont les noms des comptes et les valuers leurs account number
accounts_path = '../dat/accounts.tsv'
accounts_data = lire_Cdtr(accounts_path)
counts_name = list(accounts_data.keys())
premier_compte = counts_name[0]
print("le nom du compte : " +premier_compte, "id compte : " + accounts_data[premier_compte])


def gen_msg_id(bic: str):
    prefix = bic[:4]

    date_prefix = str(datetime.now().date().strftime('%y%m%d'))  # 2024-07-03 ==== 240703

    seq = str(msg_id_seq.gen()).zfill(6)

    return prefix + date_prefix + seq


def gen_tx_id(bic: str):
    prefix = bic[:4]

    date_prefix = str(datetime.now().date().strftime('%y%m%d'))  # 2024-07-03 ==== 240703

    seq = str(tx_id_seq.gen()).zfill(8)

    return prefix + date_prefix + seq


# remplissons le fichier xml
def remplir_xml(template, bank_name, montant_total, nombre_tx, list_template):
    bank_bic = bank_data[bank_name]
    # msgid
    MsgId = gen_msg_id(bank_bic)

    # credtTm:
    # Obtenir la date et l'heure actuelles
    now = datetime.now(timezone.utc)
    # le format voulu
    CreDtTm = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    # sum_payment 
    sum_payment = 0
    # date
    formatted_date = datetime.now().strftime('%Y-%m-%d')

    template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['MsgId'] = MsgId
    template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['CreDtTm'] = CreDtTm
    template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['NbOfTxs'] = nombre_tx
    template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['TtlIntrBkSttlmAmt']['$'] = montant_total
    template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['IntrBkSttlmDt'] = formatted_date
    template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['InstgAgt']['FinInstnId']['BICFI'] = bank_bic
    template['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf'] = list_template

    return template


def add_tx(bank_name, credit_template, montant):
    bank_bic = bank_data[bank_name]

    InstrId = gen_tx_id(bank_bic)
    credit_template['PmtId']['InstrId'] = InstrId
    credit_template['PmtId']['EndToEndId'] = InstrId
    credit_template['PmtId']['TxId'] = InstrId

    # IntrBkSttlmAmt

    IntrBkSttlmAmt = str(montant)

    credit_template['IntrBkSttlmAmt']['$'] = IntrBkSttlmAmt


    # dbtr fake
    fake = Faker()
    name = fake.name()
    credit_template['Dbtr']['Nm'] = name

    id = str(fake.bban())
    credit_template['DbtrAcct']['Id']['Othr']['Id'] = id

    credit_template['DbtrAgt']['FinInstnId']['BICFI'] = bank_bic


    # à recuperer et remplir

    accounts_name = str(random.choice(counts_name))
    credit_template['Cdtr']['Nm'] = accounts_name  
    credit_template['CdtrAcct']['Id']['Othr']['Id'] =  accounts_data[accounts_name]
    credit_template['RmtInf']['Ustrd'] = fake.text(max_nb_chars=20)

    return credit_template


def creer_xml_doc(nombre_tx, bank_name, credit_template, template):
    # initialisation
    montant_total = 0
    list_template = []  # liste des tx
    fake = Faker()

    for i in range(nombre_tx):
        montant = fake.random_number(digits=5)
        # montant = fake.pydecimal(5, 2, True)

        # créer une nouvelle copie du modèle de crédit pour chaque transaction
        current_credit_template = copy.deepcopy(credit_template)

        tx = add_tx(bank_name, current_credit_template, montant)
        list_template.append(tx)

        # print("le " + i + " eme montant est : "  , montant)
        montant_total += montant
        # print(f"le {i}-eme montant est : {montant}")
        # fake = Faker()

    temp = remplir_xml(template, bank_name, str(montant_total), str(nombre_tx), list_template)

    return temp


if __name__ == '__main__':

    for i in range(2):
        nombre_tx = random.randint(1, 20)
        bank_name = random.choice(banks_names)

        temp = creer_xml_doc(nombre_tx, bank_name, credit_template, template)

        file = f"../output/fich{i}.xml"

        with open(file, 'w', encoding='utf8') as f:
            # pac9_xsd.validate(xmltodict.unparse(pacs8_in_dict2, pretty=True, cdata_key='$'))
            f.write(xmltodict.unparse(temp, pretty=True, cdata_key='$'))

# Input
# --- InstgAgt: BIC bank
# --- MsgId, CreDtTm, NbOfTxs, IntrBkSttlmDt
#    Par payment 
#         ---- InstrId
#         ---- Dbtr: Nm, Id : gen with faker 
#         ---- Cdtr: CdtrAcct, Nm, Id : from db
#         ---- RmtInf: optional faker
