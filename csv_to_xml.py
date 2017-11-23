# -*- coding: utf-8 -*-
from lxml import etree
import csv 



#  ===  Ouverture du csv ===
# On met les infos dans une liste qui contiendra les lignes
# Une ligne est une liste de chaines de caractères
with open('ponctualite-mensuelle-transilien.csv', 'r') as f:
    rowReader = csv.reader(f,delimiter = ';')
    rows_list = list(rowReader)    
    rows_list = rows_list[1:]   # on oublie la première ligne (qui ne contient que les 
				# titres de colonnes), on passe directement à la deuxième





# ==========================================================
# ==                  Formation du XML                    ==
# ==========================================================    

XmlDoc = etree.Element("trains")
serviceRER = etree.SubElement(XmlDoc,'service')
nom_serviceRER = etree.SubElement(serviceRER,'nom_service')
nom_serviceRER.text = 'RER'
serviceTrans = etree.SubElement(XmlDoc,'service')
nom_serviceTrans = etree.SubElement(serviceTrans,'nom_service')
nom_serviceTrans.text = 'Transilien'

AddedIds = {} #On garde les Ids des trains déjà rencontrés dans une structure
    # dictionnaire ID:etree object

for row in rows_list:
    ThisId = row[0]
    # ================== Service ====================
    # Si la ligne de train en question n'existe pas deja, on l'ajoute 
    if ThisId not in AddedIds :
        lettre_ligne = row[3]
        if row[2] == 'RER':
            ligne = etree.SubElement(serviceRER,'ligne',lettre_ligne = lettre_ligne, id = ThisId)
        else: #Transilien, a priori
            ligne = etree.SubElement(serviceTrans,'ligne',lettre_ligne = lettre_ligne, id = ThisId)
        nom_ligne = etree.SubElement(ligne,'nom_ligne')
        nom_ligne.text = row[4].decode('ISO-8859-1')  # le .decode sert aux accents
        AddedIds[ThisId] = ligne  # on ajoute le couple id:objet dans le dictionnaire

    # ================== données ====================
    # on ajoute ensuite les données
    ligne = AddedIds[ThisId]   
    print(row)
    donnee = etree.SubElement(ligne,'donnee')
    Date = etree.SubElement(donnee,'Date')
    Date.text = row[1].decode('ISO-8859-1')
    Taux = etree.SubElement(donnee,'Taux')
    # On ajoute la valeur du taux, arrondie à 1 decimale près :
    roundedNumber = round(float(row[5]),1)  if row[5] != '' else ''
        # il y a une onnee vide dans les taux. On ne peut pas la convertir en 
        # float, donc on la laisse
    Taux.text = str(roundedNumber)
    
    Nombre = etree.SubElement(donnee,'Nombre')
    roundedNumber = round(float(row[6]),1)  # arrondi à 1 decimale près
    Nombre.text = str(roundedNumber)
    

document_string = (etree.tostring(XmlDoc, pretty_print=True))



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
f.write(DTD+document_string)
f.close()






