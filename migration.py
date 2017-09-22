#!/usr/bin/python3

# ubuntu abhängigkeit:
# apt install python3-mysql.connector

import sys
import mysql.connector as mc
import xml.etree.ElementTree as ET

try:
    connection = mc.connect(
         host="localhost",
         db="prosody",
         user="root", passwd="root"
        )
        
    connection2 = mc.connect(
         host="localhost",
         db="ejabberd",
         user="root", passwd="root"
        )
    
except mc.Error as e:
    print("Error %d: %s" % (e.args[0], e.args[1]))
    sys.exit(1)

cursor = connection.cursor()
cursor2 = connection2.cursor()
print("Nachrichten werden von Prosody geladen...")
cursor.execute("SELECT * FROM prosodyarchive")
result = cursor.fetchall()

format_str = """INSERT INTO archive (`username`, `timestamp`, `peer`, `bare_peer`, `xml`, `txt`, `kind`)
    VALUES ('{username}', {timestamp}, '{peer}', '{bare_peer}', '{xml}', '{txt}', 'chat');"""

anzahl = len(result)
print("Fertig geladen. Fange an umzubauen und in ejabberd zu laden.")
for r in result:
    print("Verarbeite Nachricht " + str(r[0]) + " von " + str(anzahl))

    dom = ET.fromstring(r[8])

    timestamp = str(r[5]) + "000000" # microsekunden

    if r[6].decode("utf-8") in dom.get('to'):
        peerstr = dom.get('to')
    elif r[6].decode("utf-8") in dom.get('from'):
        peerstr = dom.get('from')
    else:
        peerstr = r[6].decode("utf-8")

    text = "" # text aus xml Feld 'body'
    for bodytext in dom.findall('body'):
        if bodytext.text != None:
            text += bodytext.text

    text = text.replace("'", "&apos;") # escapen
    text = text.replace("\\", "\\\\")  # noch mehr escapen

    userName = r[2].decode("utf-8")
    barepeer = r[6].decode("utf-8")
    xmlstr = r[8].decode("utf-8")
    xmlstr = xmlstr.replace("'", "\\'") # noch mal escapen

    sql_command = format_str.format(username=userName, timestamp=timestamp, peer=peerstr, bare_peer=barepeer, xml=xmlstr, txt=text)

#    print(sql_command) # test ausgabe des sql Befehls

    cursor2.execute(sql_command)

connection2.commit()

cursor2.close()
connection2.close()
cursor.close()
connection.close()
