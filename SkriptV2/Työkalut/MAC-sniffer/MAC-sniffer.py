#!/bin/python3
#Vaatii scapyn
#sudo apt install python3-scapy
from scapy.all import *
import csv
import os

#Tehdään tiedosto jos sitä ei ole
if not os.path.exists("mac-osoitteet.csv"):
	with open('mac-osoitteet.csv', mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["Laite", "MAC-osoite"])  
		
#laitetaan CSV-tiedostosta tiedot sanakirjaan niin saadaan käytyä läpi jos tulee samoja
tallennettavat_tiedot = {}	
with open("mac-osoitteet.csv", mode='r', newline='') as file:
	reader = csv.DictReader(file)  
	for row in reader:
		laite = row['Laite']  
		mac_osoite = row['MAC-osoite']  
		tallennettavat_tiedot[laite] = mac_osoite  


file = open('mac-osoitteet.csv', mode='a', newline='')
writer = csv.writer(file)



def discover_snifferi(packet):

	if packet.haslayer(DHCP):
		for opt in packet[DHCP].options:
			#Etsitään DHCP Discover -viestejä
			if opt[0] == 'message-type' and opt[1] == 1:  # 1 = DHCP Discover
				if packet[Ether].src.startswith(vendor):
					print(f"DHCP discover macistä: {packet[Ether].src}")
					macosoite = packet[Ether].src
					if macosoite in tallennettavat_tiedot.values():
						print("\nMAC-osoite on jo listassa TESTAUSMOODISSA ELI LAITETAAN SILTI LISTAAN!")
						print("Ota # merkki pois tässä allaolevalta riviltä jos haluat ettei samoja maceja laiteta listaan")
						#break
					laite = input("Anna nimi laitteelle: ")
					tallennettavat_tiedot.update({laite:macosoite})
					#laitetaan löydetty MAC csv-tiedostoon
					writer.writerow([laite, macosoite])
		        
					break

#Katotaan DHCP paketit porttien perusteella
vendor = input("Anna MAC-osoitteen vendor osa/muutama numero alusta (tyhjä = kaikki) ")
sniff(iface="ens33", filter="udp and (port 67 or port 68)", prn=discover_snifferi, store=0)

file.close()
