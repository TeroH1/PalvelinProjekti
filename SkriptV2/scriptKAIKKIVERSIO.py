import csv
import subprocess
import time
import threading
import os


#Funktio threadingia varten
#Käytännössä tarkotus on että voi kutsua helposti 
def scriptinloppu(ip_address, nimi):
	sshlog = f"Logit/SSH_{ip_address}.txt"
	with open(sshlog, "w") as tiedosto:
		subprocess.run(['expect', 'sshtarkistus.exp', ip_address], check=True, stdout=tiedosto, stderr=tiedosto)
	print(f"{nimi} ssh tarkistus suoritettu osoitteella {ip_address} ")
	konflog = f"Logit/CONF_{ip_address}.txt"
	with open(konflog, "w") as tiedosto2:
		subprocess.run(['expect', 'konfigurointi.exp', ip_address], check=True, stdout=tiedosto2, stderr=tiedosto2)
	print(f"{nimi} konfigurointi suoritettu osoitteella {ip_address}")
	time.sleep(20)
	with open(sshlog, "w") as tiedosto:
		subprocess.run(['expect', 'sshtarkistus.exp', ip_address], check=True, stdout=tiedosto, stderr=tiedosto)
	print(f"{nimi} ssh tarkistus suoritettu osoitteella {ip_address} ")
	clustlog = f"Logit/CLUST_{ip_address}.txt"
	with open(clustlog, "w") as tiedosto3:
		subprocess.run(['expect', 'clusteri.exp', ip_address], check=True, stdout=tiedosto3, stderr=tiedosto3)
	print(f"{nimi} Clusteri.exp suoritettu osoitteella {ip_address}")
	print("------------------------------------------------------------")
	for row in rows:
		if row['Nimi'] == nimi:
			row['Konfiguroitu'] = 'True'
			with open(output_file, mode='w', newline='') as file:  # Tää on vähän huono ratkau mutta parempaa hakies toimii
				fieldnames = ['Nimi', 'MAC-osoite', 'Konfiguroitu']
				writer = csv.DictWriter(file, fieldnames=fieldnames)
				writer.writeheader() 
				writer.writerows(rows)  
				print(rows) # Debug printti


input_file = 'Tiedot.csv'
output_file = 'Tiedot2.csv'
dhcp_conf_file = '/etc/dhcp/dhcpd.conf'

		
		


static_config = """subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.100 192.168.1.150;
  option routers 192.168.1.1;
  option tftp-server-address 192.168.1.1;
  next-server 192.168.1.1;
  filename "lpxelinux.0";
  option domain-name-servers 192.168.1.1;
  option domain-name "local";
}
"""

dhcp_configurations = []

with open(input_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    rows = []
    for row in reader:
        nimi = row['Nimi']
        if row['Konfiguroitu'] == 'False':
            mac = row['MAC-osoite']
            ip_last_octet = nimi[-2:]
            ip_address = f"192.168.1.{ip_last_octet}"  # Täydellinen IP-osoite
            print(f"{nimi} laitteen konfigurointi aloitettu")
            print(f"MAC-osoite on: {mac}")
            print(f"IP-osoite on: {ip_last_octet}")
            dhcp_configurations.append(f"""host {nimi} {{
  hardware ethernet {mac}; 
  server-name "host1"; 
  filename "PVEXXX/lpxelinux.0"; 
  fixed-address {ip_address};
}}""")
        else:
            print(f"{nimi} laite ON JO konfiguroitu")
        rows.append(row)




with open(dhcp_conf_file, mode='w') as file:
    file.write(static_config)
    for config in dhcp_configurations:
        file.write(config + "\n")

print(f"dhcpd.conf-tiedosto '{dhcp_conf_file}' on päivitetty.")

subprocess.run(['sudo', 'systemctl', 'restart', 'isc-dhcp-server.service'], check=True)
print("DHCP-palvelin uudelleenkäynnistetty, käynnistä palvelin")
print("--------------------------------------------")


threads = []
for row in rows:
    if row['Konfiguroitu'] == 'False':
        ip_last_octet = row['Nimi'][-2:]
        ip_address = f"192.168.1.{ip_last_octet}"
        nimi = row['Nimi']
        thread = threading.Thread(target=scriptinloppu, args=(ip_address, nimi,))
        threads.append(thread) #lisätään listaan jotta voidaan seurata millon kaikki on valmiita
        thread.start()

#Odotetaan että threadit on valmiita
for thread in threads:
	thread.join()
	
