#! /usr/bin/env python
import xmlschema # type: ignore
from pprint import pprint
# import faker
import xmltodict # type: ignore

SCHEMA_PAC8 = 'doc_xsd/pacs.008.001.07.xsd'

pac9_xsd = xmlschema.XMLSchema(SCHEMA_PAC8)


# def validate_xml_file():
#     with open('../doc_xml/Credit.ICF.IBMRMRMR240614103511043.I.xml', encoding='utf8') as f:
#         file_content = f.read()

#         pac9_xsd.validate(file_content)

#         pacs8_in_dict = pac9_xsd.to_dict(file_content)

#         # pprint(pacs8_in_dict, sort_dicts=False)

#         pacs8_in_dict['FIToFICstmrCdtTrf']['GrpHdr']['MsgId'] = 'BCM'

#         pacs8_in_xml = pac9_xsd.to_etree(pacs8_in_dict)
#         filestr = xmlschema.etree_tostring(pacs8_in_xml)


def read_and_edit_xml_file():
    with open('doc_xml\Credit.ICF.IBMRMRMR240614103511043.I.xml', encoding='utf8') as f:
        file_content = f.read()
    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$')

    pacs8_in_dict2 = xmltodict.parse(file_content, cdata_key='$')
    pprint(pacs8_in_dict2, sort_dicts=False)


    i =2
    montant = 200



    with open('outsp.xml', 'w', encoding='utf8') as f:
        pac9_xsd.validate(xmltodict.unparse(pacs8_in_dict2, pretty=True, cdata_key='$'))
        f.write(xmltodict.unparse(pacs8_in_dict2, pretty=True, cdata_key='$'))


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



if __name__ == '__main__':
    read_and_edit_xml_file()
