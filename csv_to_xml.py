# -*- coding: utf-8 -*-
from lxml import etree
import csv 

with open('ponctualite-mensuelle-transilien.csv') as f:
    f.next()  # on oublie la première ligne, on passe directement à la deuxième
    rowReader = csv.reader(f,delimiter = ';')
    print(type(rowReader))
    rows_list = list(rowReader)    
    rows_list = sorted(rows_list, key=lambda col:(col[2],col[0]) )  
        # on trie, d'abord par service (3eme colonne), puis par id de train (1ere colonne)
    current_service = ''
    current_id = ''    
    
    XmlDoc = etree.root("trains")    
    servicelist = []    
    
    
    for row in rows_list: 
        Service = row[2]
        Id = row[0]
        print(row)
        body = etree.SubElement(html, "body")
        body.text = "TEXT"














