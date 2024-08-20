#! /usr/bin/env python
import os
import xmlschema
import xmltodict
from pprint import pprint

SCHEMA_PAC8 = 'myapp/pacs.008.001.07.xsd'
# décodage 
schema = xmlschema.XMLSchema(SCHEMA_PAC8)



def vailde_xml(file) :

    with open(file, encoding='utf8') as f:
        file_content = f.read()
        schema.validate(file_content)



    # Valider le document XML par rapport au schéma
    try:
        schema.validate(file_content)
        print(f"Le document XML {file} est valide par rapport au schéma XSD.") 

        return True
    
    except xmlschema.XMLSchemaValidationError as e:
        print("Le document XML n'est pas valide par rapport au schéma XSD :")
        print(str(e))
        print("errer dans " + file)
        return False
    


# Chemin vers le répertoire contenant les fichiers XML à valider
directory_path = 'output'

# Parcourir les fichiers dans le répertoire spécifié
for filename in os.listdir(directory_path):
    
    file_path = os.path.join(directory_path, filename)
    vailde_xml(file_path)