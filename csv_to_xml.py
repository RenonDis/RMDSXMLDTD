# -*- coding: utf-8 -*-
from lxml import etree
import csv 

    

with open('ponctualite-mensuelle-transilien.csv') as f:
    f.next()  # on oublie la première ligne, on passe directement à la deuxième
    rowReader = csv.reader(f,delimiter = ';')
    print(type(rowReader))
    rows_list = list(rowReader)    
        # on trie, d'abord par service (3eme colonne), puis par id de train (1ere colonne)
    current_service = ''
    current_id = ''    
    
    """
    for row in rows_list: 
        Service = row[2]
        Id = row[0]
        print(row)
        body = etree.SubElement(html, "body")
        body.text = "TEXT"
"""


XmlDoc = etree.Element("root")
serviceRER = etree.SubElement(XmlDoc,'service')
serviceTrans = etree.SubElement(XmlDoc,'service')
AddedIds = {} # keep track of the Ids of the trains we already added to the structure
    # dictionnary ID:etree object
for row in rows_list:
    print(row)
#    row = [replace_accents(x) for x in row]
    ThisId = row[0] 
    if ThisId not in AddedIds :
        if row[2] == 'RER':
            ligne = etree.SubElement(serviceRER,'ligne')
            nom_ligne = etree.SubElement(ligne,'nom_ligne')
            nom_ligne.text = row[4]
            AddedIds[ThisId] = ligne  # on ajoute le couple id:objet dans le dictionnaire
        else: #Transilien, a priori
            ligne = etree.SubElement(serviceTrans,'ligne')
            nom_ligne = etree.SubElement(ligne,'nom_ligne')
            nom_ligne.text = row[4]
            AddedIds[ThisId] = ligne  # on ajoute le couple id:objet dans le dictionnaire

print(etree.tostring(XmlDoc, pretty_print=True,  encoding='iso-8859-1'))










































