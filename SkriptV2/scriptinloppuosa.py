#!/usr/bin/python3
import csv
import subprocess
import time
import sys
ip_address = sys.argv[1]
nimi = sys.argv[2]

subprocess.run(['expect', 'sshtarkistus.exp', ip_address], check=True)
print(f"{nimi} ssh tarkistus suoritettu osoitteella {ip_address} ")
subprocess.run(['expect', 'konfigurointi.exp', ip_address], check=True)
print(f"{nimi} konfigurointi suoritettu osoitteella {ip_address}")
time.sleep(20)
subprocess.run(['expect', 'sshtarkistus.exp', ip_address], check=True)
print(f"{nimi} ssh tarkistus suoritettu osoitteella {ip_address} ")
subprocess.run(['expect', 'clusteri.exp', ip_address], check=True)
print(f"{nimi} Clusteri.exp suoritettu osoitteella {ip_address}")
print("------------------------------------------------------------")

