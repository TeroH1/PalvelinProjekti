#!/bin/python3
#Vaatii scapyn
#sudo apt install python3-scapy
from scapy.all import *
import csv
import os
interface = "ens33"
#Muuttuja joka seuraa tällä kerralla tulleita MAC osotteita
sessioMACosoitteet = {}

#Tehdään tiedosto jos sitä ei ole
if not os.path.exists("mac-osoitteet.csv"):
	with open('mac-osoitteet.csv', mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["Nimi", "MAC-osoite", "PVEn-ip", "Loopback", "PrimaryLink-ip", "SecondaryLink-ip", "Subnet", "PrimaryLink-naapuri", "SecondaryLink-naapuri", "Konfiguroitu"])  
		
#laitetaan CSV-tiedostosta tiedot sanakirjaan niin saadaan käytyä läpi jos tulee samoja
tallennettavat_tiedot = {}	
with open("mac-osoitteet.csv", mode='r', newline='') as file:
	reader = csv.DictReader(file)  
	for row in reader:
		laite = row['Nimi']  
		mac_osoite = row['MAC-osoite']
		ipaddress = row['PVEn-ip']       
		loopback = row['Loopback']
		primarylinkip = row['PrimaryLink-ip']
		secondarylinkip = row['SecondaryLink-ip']
		subnet = row['Subnet']
		primaryneighborip = row['PrimaryLink-naapuri']
		secondaryneighborip = row['SecondaryLink-naapuri']
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
					if macosoite in tallennettavat_tiedot.values() or macosoite in sessioMACosoitteet.values():
						print(f"\nMAC-osoite on jo listassa nimellä:\n")
						for avain, arvo in tallennettavat_tiedot.items():
							if arvo == macosoite:
								print(f"{avain}	--- Aiemmalla sessiolla lisätty")
						
						for avain, arvo in sessioMACosoitteet.items():
							if arvo == macosoite:
								print(f"{avain}	--- Tällä sessiolla lisätty")
							
						break
					
					#NIMI
					print("HUOM nimi täytyy olla kirjoitettu pienillä kirjaimilla (esim pvexx)")
					laite = input("Anna nimi laitteelle: ")
					sessioMACosoitteet[laite] = macosoite 
					tallennettavat_tiedot.update({laite:macosoite})
					
					#ipaddress
					ipaddress = input("Anna laitteelle IP osoite, jota käytetään ssh yhteyksiin skriptin suorittamiseksi (esim 192.168.1.11): ")
					tallennettavat_tiedot.update({laite:ipaddress})
					
					#LOOPBACK OSOITE
					loopback = input(f"{laite} - anna loopback osoite BGP yhteyttä varten (muodossa 10.2.1.48): ")
					tallennettavat_tiedot.update({laite:loopback})
					
					#Primary LINK-IP
					#Huom. print
					print("\nHUOM!!!!!!!!!\n LINK IP-OSOITTEITA VAADITAAN 2!")
					primarylinkip = input(f" - {laite} - Anna BGP yhteyttä varten oma Primary leaf Link-ip muodossa 10.10.1.97: ")
					tallennettavat_tiedot.update({laite:primarylinkip})
					
					#SECONDARY LINK-IP
					secondarylinkip = input(f" - {laite} - Anna BGP yhteyttä varten oma SECONDARY leaf Link-ip muodossa 10.10.2.97:  ")
					tallennettavat_tiedot.update({laite:secondarylinkip})
					
					
					#Subnet
					subnet = input(f" - {laite} - anna BGP leaf naapuriverkon subnet (muodossa esim '31' ):\n ")
					tallennettavat_tiedot.update({laite:subnet})
					
					#PRIMARY link-ip naapurin osoite
					print("\nHUOM!!!!\n NAAPUREIDEN OSOITTEITA VAADITAAN 2!")
					primaryneighborip = input(f" - {laite} - anna BGP leaf naapurin ip osoite (muodossa 10.10.1.96):\n ")
					tallennettavat_tiedot.update({laite:primaryneighborip})
					
					#SECONDARY link-ip naapurin osoite
					secondaryneighborip = input(f" - {laite} - anna BGP leaf naapurin ip osoite (muodossa 10.10.2.96):\n ")
					tallennettavat_tiedot.update({laite:primaryneighborip})
				
					
					konfiguroitu = "False"
					tallennettavat_tiedot.update({laite:konfiguroitu})
					#laitetaan tiedot csv-tiedostoon
					writer.writerow([laite, macosoite, ipaddress,  loopback, primarylinkip, secondarylinkip, subnet, primaryneighborip, secondaryneighborip, konfiguroitu])
					print(f"\n!\nTiedot vastaanotettu, Kuunnellaan seuraavaa DHCP-pakettia\n!\n")
		        
					break

#Katotaan DHCP paketit porttien perusteella
vendor = input("Anna MAC-osoitteen vendor osa/muutama numero alusta (tyhjä = kaikki)(dell 14:18:77)")
sniff(iface=interface, filter="udp and (port 67 or port 68)", prn=discover_snifferi, store=0)

file.close()
