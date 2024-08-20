from django.shortcuts import render, redirect
from .models import MsgIDSeq, Bank, Account
from .forms import TransactionForm
import xml.etree.ElementTree as ET
import os

# Vue pour la page d'accueil
def index(request):
    return render(request, 'myapp/index.html')

# V<ue pour générer le fichier XML à partir du formulaire

# def generateTemplate(request):
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             bank = form.cleaned_data['bank']
#             account = form.cleaned_data['account']
#             amount = form.cleaned_data['amount']
#             account_id = form.cleaned_data['account_id']
#
#
#             account_id_value = None
#             if account_id == 'OLD_ACNT_NUM':
#                 account_id_value = account.old_acnt_num
#             elif account_id == 'ACNT_NUM':
#                 account_id_value = account.acnt_num
#             elif account_id == 'OLD_RIB':
#                 account_id_value = account.old_rib
#             elif account_id == 'NEW_RIB':
#                 account_id_value = account.new_rib
#
#
#             # Retrieve or create msg_id_seq
#             msg_id_seq, created = MsgIDSeq.objects.get_or_create(
#                 defaults={'msg_id_seq': 1}
#             )
#             current_msg_id_seq = msg_id_seq.msg_id_seq
#
#             #----------------------------------------------------------------brouillon--------------------------------------------------------------
#             # !/usr/bin/env python
#
#             import xmltodict  # type: ignore
#             import datetime
#             import xmlschema  # type: ignore
#             from pprint import pprint
#             from datetime import datetime, timezone
#             from faker import Faker
#             import random
#             import copy
#
#             SCHEMA_PAC8 = 'myapp\pacs.008.001.07.xsd'
#
#             pac9_xsd = xmlschema.XMLSchema(SCHEMA_PAC8)
#
#             # pour avoir une séquence variable
#
#
#             template = {'Document': {'@xmlns': 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.07',
#                                      '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
#                                      'FIToFICstmrCdtTrf': {'GrpHdr': {'MsgId': None,
#                                                                       'CreDtTm': None,
#                                                                       'NbOfTxs': None,
#                                                                       'TtlIntrBkSttlmAmt': {'@Ccy': 'MRU',
#                                                                                             '$': None},
#                                                                       'IntrBkSttlmDt': None,
#                                                                       'SttlmInf': {'SttlmMtd': 'CLRG',
#                                                                                    'ClrSys': {'Prtry': 'ACH'}},
#                                                                       'InstgAgt': {'FinInstnId': {'BICFI': None}}},
#                                                            'CdtTrfTxInf': [None]
#                                                            }
#                                      }
#                         }
#
#             credit_template = {'PmtId': {'InstrId': '',
#                                          'EndToEndId': '',
#                                          'TxId': ''},
#                                'PmtTpInf': {'SvcLvl': {'Cd': 'SEPA'},
#                                             'LclInstrm': {'Cd': 'B2B'},
#                                             'CtgyPurp': {'Cd': 'CASH'}},
#                                'IntrBkSttlmAmt': {'@Ccy': 'MRU',
#                                                   '$': None},
#                                'ChrgBr': 'SLEV',
#                                'Dbtr': {'Nm': None},
#                                'DbtrAcct': {'Id': {'Othr': {'Id': None}}},
#                                'DbtrAgt': {'FinInstnId': {'BICFI': None}},
#                                'CdtrAgt': {'FinInstnId': {'BICFI': 'BCEMMRMR'}},
#                                'Cdtr': {'Nm': None},
#                                'CdtrAcct': {'Id': {'Othr': {'Id': None}}},
#                                'Purp': {'Cd': 'ADVA'},
#                                'RmtInf': {'Ustrd': None}}
#
#             # recuperer les bic des banks
#
#
#             def gen_msg_id(bic: str):
#                 prefix = bic[:4]
#
#                 date_prefix = str(datetime.now().date().strftime('%y%m%d'))  # 2024-07-03 ==== 240703
#
#                 # seq = str(msg_id_seq.gen()).zfill(6)
#                 seq = str(current_msg_id_seq).zfill(6)
#
#                 return prefix + date_prefix + seq
#
#             def gen_tx_id(bic: str):
#                 prefix = bic[:4]
#
#                 date_prefix = str(datetime.now().date().strftime('%y%m%d'))  # 2024-07-03 ==== 240703
#                 tx_id_seq = 2*current_msg_id_seq
#                 seq = str(tx_id_seq).zfill(8)
#
#                 return prefix + date_prefix + seq
#
#             # remplissons le fichier xml
#             def remplir_xml(bank_name, montant_total, nombre_tx, list_template):
#
#                 # bank_bic = bank_data[bank_name]
#                 bankk = Bank.objects.get(bank_name=bank_name)
#                 bank_bic = bankk.bank_id  # Récupérer le BIC
#
#
#                 # msgid
#                 MsgId = gen_msg_id(bank_bic)
#
#                 # credtTm:
#                 # Obtenir la date et l'heure actuelles
#                 now = datetime.now(timezone.utc)
#                 # le format voulu
#                 CreDtTm = now.strftime('%Y-%m-%dT%H:%M:%SZ')
#
#                 # nombre de transactions
#                 NbOfTxs = str(len(list_template))
#                 # sum_payment
#                 sum_payment = 0
#                 # date
#                 formatted_date = datetime.now().strftime('%Y-%m-%d')
#
#                 template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['MsgId'] = MsgId
#                 template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['CreDtTm'] = CreDtTm
#                 template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['NbOfTxs'] = nombre_tx
#                 template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['TtlIntrBkSttlmAmt']['$'] = montant_total
#                 template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['IntrBkSttlmDt'] = formatted_date
#                 template['Document']['FIToFICstmrCdtTrf']['GrpHdr']['InstgAgt']['FinInstnId']['BICFI'] = bank_bic
#                 template['Document']['FIToFICstmrCdtTrf']['CdtTrfTxInf'] = list_template
#
#                 return template
#
#             def add_tx(bank_name, credit_template, montant):
#                 # bank_bic = bank_data[bank_name]
#                 bankk = Bank.objects.get(bank_name=bank)
#                 bank_bic = bankk.bank_id  # Récupérer le BIC
#
#                 InstrId = gen_tx_id(bank_bic)
#                 credit_template['PmtId']['InstrId'] = InstrId
#                 credit_template['PmtId']['EndToEndId'] = InstrId
#                 credit_template['PmtId']['TxId'] = InstrId
#
#                 # IntrBkSttlmAmt
#
#                 IntrBkSttlmAmt = str(montant)
#
#                 credit_template['IntrBkSttlmAmt']['$'] = IntrBkSttlmAmt
#
#                 # dbtr fake
#                 fake = Faker()
#                 name = fake.name()
#                 credit_template['Dbtr']['Nm'] = name
#
#                 id = str(fake.bban())
#                 credit_template['DbtrAcct']['Id']['Othr']['Id'] = id
#
#                 credit_template['DbtrAgt']['FinInstnId']['BICFI'] = bank_bic
#
#                 # à recuperer et remplir
#
#                 # accounts_name = str(random.choice(counts_name))
#                 accounts_name = account
#                 credit_template['Cdtr']['Nm'] = accounts_name
#
#                 # id à choisr parmiles ids de accounts_name
#                 # credit_template['CdtrAcct']['Id']['Othr']['Id'] =  random.choice(accounts_data[accounts_name])
#                 credit_template['CdtrAcct']['Id']['Othr']['Id'] = account_id_value
#
#                 credit_template['RmtInf']['Ustrd'] = fake.text(max_nb_chars=20)
#
#                 return credit_template
#
#             def creer_xml_doc(nombre_tx, bank_name):
#
#                 # initialisation
#                 montant_total = 0
#                 list_template = []  # liste des transactions
#                 # fake = Faker()
#                 # montant = fake.random_number(digits=5)
#
#                 # c'est le montant saisi sur le temlpate
#                 montant = amount
#
#                 # for i in range(nombre_tx):
#                 #     # créer une nouvelle copie du modèle de crédit pour chaque transaction
#                 #     current_credit_template = copy.deepcopy(credit_template)
#                 #
#                 #     tx = add_tx(bank_name, current_credit_template, montant)
#                 #     list_template.append(tx)
#                 #
#                 #     # print("le " + i + " eme montant est : "  , montant)
#                 #     montant_total += montant
#                 #
#                 #     montant = fake.random_number(digits=5)
#
#                 # ajouter une transaction à la liste des transactions
#                 current_credit_template = copy.deepcopy(credit_template)
#                 tx = add_tx(bank, current_credit_template, montant)
#                 list_template.append(tx)
#
#                 # print("le " + i + " eme montant est : "  , montant)
#                 montant_total += montant
#
#                 temp = remplir_xml(bank_name, str(montant_total), str(len(list_template)), list_template)
#
#                 return temp
#             # if __name__ == '__main__':
#
# # -----------------------------------------------fin brouillion-------------------------------------------------------------------------------
#
#             # temp = creer_xml_doc(nombre_tx=1, bank_name = bank, credit_template, template)
#             temp = creer_xml_doc(nombre_tx=1, bank_name=bank)
#             file = f"output/fich{0}.xml"
#             with open(file, 'w', encoding='utf8') as f:
#                 # pac9_xsd.validate(xmltodict.unparse(pacs8_in_dict2, pretty=True, cdata_key='$'))
#                 f.write(xmltodict.unparse(temp, pretty=True, cdata_key='$'))
#
#             msg_id_seq.msg_id_seq += 1
#             msg_id_seq.save()
#
#             # Generate XML file
#             return redirect('index')
#     else:
#         form = TransactionForm()
#
#     return render(request, 'myapp/generateTemplate.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import TransactionForm
from .models import MsgIDSeq, Bank
import xml.etree.ElementTree as ET
import xmltodict  # type: ignore
import datetime
from datetime import datetime, timezone
from faker import Faker
import random
import copy
import os

def generateTemplate(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            bank = form.cleaned_data['bank']
            account = form.cleaned_data['account']
            amount = form.cleaned_data['amount']
            account_id = form.cleaned_data['account_id']

            # Mapping the account_id to the corresponding field
            account_id_value = getattr(account, account_id.lower())

            # Retrieve or create the list_template in session
            list_template = request.session.get('list_template', [])

            # Create the credit template

            msg_id_seq, created = MsgIDSeq.objects.get_or_create(defaults={'msg_id_seq': 1})
            current_msg_id_seq = msg_id_seq.msg_id_seq
            InstrId =gen_tx_id(bank.bank_id, current_msg_id_seq)

            # dbtr fake
            fake = Faker()



            credit_template = {
                'PmtId': {'InstrId': InstrId, 'EndToEndId': InstrId, 'TxId': InstrId},
                'PmtTpInf': {'SvcLvl': {'Cd': 'SEPA'}, 'LclInstrm': {'Cd': 'B2B'}, 'CtgyPurp': {'Cd': 'CASH'}},
                'IntrBkSttlmAmt': {'@Ccy': 'MRU', '$': str(amount)},  # Stocker en tant que str pour le XML
                'ChrgBr': 'SLEV',
                'Dbtr': {'Nm': fake.name()},
                'DbtrAcct': {'Id': {'Othr': {'Id': str(fake.bban())}}},
                'DbtrAgt': {'FinInstnId': {'BICFI': bank.bank_id}},
                'CdtrAgt': {'FinInstnId': {'BICFI': 'BCEMMRMR'}},
                'Cdtr': {'Nm': account.account_name},
                'CdtrAcct': {'Id': {'Othr': {'Id': account_id_value}}},
                'Purp': {'Cd': 'ADVA'},
                'RmtInf': {'Ustrd': Faker().text(max_nb_chars=20)}
            }

            # Add transaction to list_template
            list_template.append(credit_template)

            # Save the list_template back to the session
            request.session['list_template'] = list_template

            # Check if the user wants to finalize the transactions
            if 'finalize' in request.POST:
                # Retrieve or create msg_id_seq
                msg_id_seq, created = MsgIDSeq.objects.get_or_create(defaults={'msg_id_seq': 1})
                current_msg_id_seq = msg_id_seq.msg_id_seq

                # Calculate the total amount
                total_amount = sum([float(tx['IntrBkSttlmAmt']['$']) for tx in list_template])

                # Generate XML file
                template = {
                    'Document': {
                        '@xmlns': 'urn:iso:std:iso:20022:tech:xsd:pacs.008.001.07',
                        '@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                        'FIToFICstmrCdtTrf': {
                            'GrpHdr': {
                                'MsgId': gen_msg_id(bank.bank_id, current_msg_id_seq),
                                'CreDtTm': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                                'NbOfTxs': str(len(list_template)),
                                'TtlIntrBkSttlmAmt': {'@Ccy': 'MRU', '$': str(total_amount)},  # Conversion en str pour le XML
                                'IntrBkSttlmDt': datetime.now().strftime('%Y-%m-%d'),
                                'SttlmInf': {'SttlmMtd': 'CLRG', 'ClrSys': {'Prtry': 'ACH'}},
                                'InstgAgt': {'FinInstnId': {'BICFI': bank.bank_id}}
                            },
                            'CdtTrfTxInf': list_template
                        }
                    }
                }

                output_path = os.path.join('output', f'transaction_{current_msg_id_seq}.xml')
                with open(output_path, 'w', encoding='utf8') as f:
                    f.write(xmltodict.unparse(template, pretty=True, cdata_key='$'))

                # Clear the session list_template
                request.session.pop('list_template', None)

                # Update and save the msg_id_seq
                msg_id_seq.msg_id_seq += 1
                msg_id_seq.save()

                return redirect('index')

            return redirect('generateTemplate')

    else:
        form = TransactionForm()

    return render(request, 'myapp/generateTemplate.html', {'form': form})


def gen_msg_id(bic: str, seq: int):
    prefix = bic[:4]
    date_prefix = datetime.now().date().strftime('%y%m%d')
    return f"{prefix}{date_prefix}{str(seq).zfill(6)}"


def gen_tx_id(bic: str, seq: int):
    prefix = bic[:4]
    date_prefix = datetime.now().date().strftime('%y%m%d')
    return f"{prefix}{date_prefix}{str(seq).zfill(6)}"

# Vue pour afficher le formulaire d'ajout de transaction
def add_transaction(request):
    form = TransactionForm()
    return render(request, 'myapp/add_transaction.html', {'form': form})


from django.http import JsonResponse
from .models import Account

def ajax_load_accounts(request):
    bank_id = request.GET.get('bank')
    accounts = Account.objects.filter(bank_id=bank_id).order_by('account_name')
    return JsonResponse(list(accounts.values('id', 'account_name')), safe=False)






     # trash
# if __name__ == '__main__':
#
#     for i in range(100):
#         nombre_tx = random.randint(1, 20)
#         bank_name = random.choice(banks_names)
#
#         temp = creer_xml_doc(nombre_tx, bank_name, credit_template, template)
#
#         file = f"output/fich{i}.xml"
#
#         with open(file, 'w', encoding='utf8') as f:
#             # pac9_xsd.validate(xmltodict.unparse(pacs8_in_dict2, pretty=True, cdata_key='$'))
#             f.write(xmltodict.unparse(temp, pretty=True, cdata_key='$'))

# Input
# --- InstgAgt: BIC bank
# --- MsgId, CreDtTm, NbOfTxs, IntrBkSttlmDt
#    Par payment
#         ---- InstrId
#         ---- Dbtr: Nm, Id : gen with faker
#         ---- Cdtr: CdtrAcct, Nm, Id : from db
#         ---- RmtInf: optional faker




# Generate XML file
            # root = ET.Element("Transaction")
            # ET.SubElement(root, "Bank").text = bank.bank_name
            # ET.SubElement(root, "Account").text = account.account_name
            # ET.SubElement(root, "Amount").text = str(amount)
            # ET.SubElement(root, "AccountID").text = account_id
            # ET.SubElement(root, "MsgIDSeq").text = str(current_msg_id_seq)
            #
            # tree = ET.ElementTree(root)
            # output_path = os.path.join('output', f'transaction_{current_msg_id_seq}.xml')
            # tree.write(output_path)





# recuperer les bic des banks
            # def banks_data(banks_path):
            #
            #     banks_data = {}
            #     with open(banks_path, 'r') as f:
            #         # Lire et l'ignorer  la première ligne qui contient (bic name)
            #         header = f.readline()
            #
            #         # passons au reste du fichier en passant ligne par ligne
            #         for line in f:
            #             bic, name = line.strip().split('\t')
            #             banks_data[name] = bic
            #
            #     return banks_data

            # def lire_Cdtr(fichier):
            #     Cdtr = {}
            #     with open(fichier, 'r', encoding='utf-8') as f:
            #         # Lire et ignorer la première ligne (en-tête)
            #         en_tete = f.readline()
            #
            #         # Parcourir le reste du fichier ligne par ligne
            #         for ligne in f:
            #             # Séparer les éléments de la ligne par tabulation
            #             elements = ligne.strip().split('\t')
            #             # Assigner les valeurs aux variables
            #             nom, numero_compte = elements[2], elements[1]
            #
            #             # Ajouter au dictionnaire
            #             Cdtr[nom] = numero_compte
            #             # Cdtr[nom] = list(ligne[0], ligne[1], ligne[4], ligne[5])
            #
            #     return Cdtr

            # initialiser un objet de la classe MsgIdSeq
            # msg_id_seq = MsgIdSeq()
            # tx_id_seq = MsgIdSeq()
            #
            # # dictionnaire dont les clés sont les noms des banques et les valuers leurs bic
            # banks_path = 'dat/banks.tsv'
            # bank_data = banks_data(banks_path)
            # banks_names = list(bank_data.keys())
            #
            # # dictionnaire dont les clés sont les noms des comptes et les valuers leurs account number
            # accounts_path = 'dat/accounts.tsv'
            # accounts_data = lire_Cdtr(accounts_path)
            # counts_name = list(accounts_data.keys())

            # premier_compte = counts_name[0]
            # print("le nom du compte : " +premier_compte, "id compte : " + accounts_data[premier_compte])




# pour avoir une séquence variable

            # class MsgIdSeq:
            #     def __init__(self) -> None:
            #         self._seq = 0
            #
            #     def gen(self):
            #         self._seq += 1
            #
            #         return self._seq