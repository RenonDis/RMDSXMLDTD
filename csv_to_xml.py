# -*- coding: utf-8 -*-
from lxml import etree
import csv 




with open('ponctualite-mensuelle-transilien.csv', 'r') as f:
    rowReader = csv.reader(f,delimiter = ';')
    rows_list = list(rowReader)    
    rows_list = rows_list[1:]  # on oublie la première ligne, on passe directement à la deuxième

for row in rows_list :
    #row = [x.decode('ISO-8859-1') for x in row]
    print(row)
    for x in row:
        print(x)
    
    

XmlDoc = etree.Element("trains")
serviceRER = etree.SubElement(XmlDoc,'service')
nom_serviceRER = etree.SubElement(serviceRER,'nom_service')
nom_serviceRER.text = 'RER'
serviceTrans = etree.SubElement(XmlDoc,'service')
nom_serviceTrans = etree.SubElement(serviceTrans,'nom_service')
nom_serviceTrans.text = 'Transilien'

AddedIds = {} # keep track of the Ids of the trains we already added to the structure
    # dictionnary ID:etree object
for row in rows_list:

    ThisId = row[0]
    # ================== Service ====================
    # Si la ligne en question n'existe pas deja, on l'ajoute 
    if ThisId not in AddedIds :
        lettre_ligne = row[3]
        if row[2] == 'RER':
            ligne = etree.SubElement(serviceRER,'ligne',lettre_ligne = lettre_ligne, id = ThisId)
        else: #Transilien, a priori
            ligne = etree.SubElement(serviceTrans,'ligne',lettre_ligne = lettre_ligne, id = ThisId)
        nom_ligne = etree.SubElement(ligne,'nom_ligne')
        nom_ligne.text = row[4].decode('ISO-8859-1')  # le .decode sert aux accents
        AddedIds[ThisId] = ligne  # on ajoute le couple id:objet dans le dictionnaire

    # ================== donees ====================
    ligne = AddedIds[ThisId]   
    print(row)
    donnee = etree.SubElement(ligne,'donnee')
    Date = etree.SubElement(donnee,'Date')
    Date.text = row[1].decode('ISO-8859-1')
    Taux = etree.SubElement(donnee,'Taux')
    #roundedNumber = round(float(row[5]),1)  # a 1 decimale pres
    #Taux.text = str(roundedNumber)
    Taux.text  = row[5]
    Nombre = etree.SubElement(donnee,'Nombre')
    #roundedNumber = round(float(row[6]),1)  # a 1 decimale pres
    #Nombre.text = str(roundedNumber)
    Nombre.text = row[6]


s = (etree.tostring(XmlDoc, pretty_print=True))



DTD = """<?xml version="1.0" encoding="ISO-8859-1"?>

<!DOCTYPE trains [
<!ELEMENT trains (service+)>
<!ELEMENT service (nom_service,ligne+)>
        <!ELEMENT nom_service (#PCDATA)>

        <!ATTLIST ligne
                id CDATA  #REQUIRED
                lettre_ligne CDATA  #REQUIRED >
        <!ELEMENT ligne (nom_ligne,donnee+)>
                <!ELEMENT nom_ligne (#PCDATA)>
                <!ELEMENT donnee (Date,Taux,Nombre)>
                        <!ELEMENT Date (#PCDATA)>
                        <!ELEMENT Taux (#PCDATA)>
                        <!ELEMENT Nombre (#PCDATA)>
]>
"""







f = open('ponctualite-mensuelle-transilien.xml','w')
f.write(DTD+s)
f.close()








































