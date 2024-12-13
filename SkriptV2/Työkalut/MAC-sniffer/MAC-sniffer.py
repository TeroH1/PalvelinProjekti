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
		writer.writerow(["Nimi", "MAC-osoite","Loopback","Link-ip/subnet", "Link-naapuri"])  
		
#laitetaan CSV-tiedostosta tiedot sanakirjaan niin saadaan käytyä läpi jos tulee samoja
tallennettavat_tiedot = {}	
with open("mac-osoitteet.csv", mode='r', newline='') as file:
	reader = csv.DictReader(file)  
	for row in reader:
		laite = row['Nimi']  
		mac_osoite = row['MAC-osoite']
		loopback = row['Loopback']
		linkip = row['Link-ip/subnet']
		linknaapuri = row['Link-naapuri']
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
					laite = input("Anna nimi laitteelle(PVExx): ")
					tallennettavat_tiedot.update({laite:macosoite})
					loopback = input(f"{laite} - anna loopback osoite BGP yhteyttä varten (muodossa 10.2.1.48)=: ")
					tallennettavat_tiedot.update({laite:loopback})
					
					#Huom. print
					print("\nHUOM!!!!!!!!!\nLinkip:stä käytetään vain loppuosaa, koska redunttanttinen yhteys eli myös 2.96/31 käytetään")
					linkip = input(f" - {laite} - anna laitteen SFP-interfacejen osoite BGP yhteyttä varten (muodossa 10.10.1.96/31): ")
					tallennettavat_tiedot.update({laite:linkip})
					
					#Huom. print
					print("\nHUOM!!!!!!!!!\nLinknaapurista käytetään vain loppuosaa, koska redunttanttinen yhteys eli myös 2.96 käytetään")
					linknaapuri = input(f" - {laite} - anna BGP leaf naapurin ip osoite (muodossa 10.10.1.96): ")
					tallennettavat_tiedot.update({laite:linknaapuri})
					#laitetaan tiedot csv-tiedostoon
					writer.writerow([laite, macosoite, loopback, linkip, linknaapuri])
		        
					break

#Katotaan DHCP paketit porttien perusteella
vendor = input("Anna MAC-osoitteen vendor osa/muutama numero alusta (tyhjä = kaikki)(dell 14:18:77)")
sniff(iface="ens33", filter="udp and (port 67 or port 68)", prn=discover_snifferi, store=0)

file.close()
