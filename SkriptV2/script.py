import csv
import subprocess
import time
#Test

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
            row['Konfiguroitu'] = 'True'
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

with open(output_file, mode='w', newline='') as file:
    fieldnames = ['Nimi', 'MAC-osoite', 'Konfiguroitu']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"CSV-tiedosto '{output_file}' on päivitetty.")

with open(dhcp_conf_file, mode='w') as file:
    file.write(static_config)
    for config in dhcp_configurations:
        file.write(config + "\n")

print(f"dhcpd.conf-tiedosto '{dhcp_conf_file}' on päivitetty.")

subprocess.run(['sudo', 'systemctl', 'restart', 'isc-dhcp-server.service'], check=True)
print("DHCP-palvelin uudelleenkäynnistetty, käynnistä palvelin")

# Tässä käytetään jo aiemmin käytettyä muuttujaa rows, eli siellä on myös nodet joiden arvo on alkujaankin ollut true
# Korjaus voi olla ettei vaihdeta aluksi konfiguroinnissa True->False vaan vasta tässäkohti
# Sillee menis falset kuitenkin läpi, truet ei ja tää kohta voitas muuttaa if row['konfiguroitu'] == False: 
print("--------------------------------------------")
print(rows)
for row in rows:
    if row['Konfiguroitu'] == 'True':
        ip_last_octet = row['Nimi'][-2:]
        ip_address = f"192.168.1.{ip_last_octet}"
        subprocess.run(['expect', 'sshtarkistus.exp', ip_address], check=True)
        print(f"{row['Nimi']} ssh tarkistus suoritettu osoitteella {ip_address} ")
        subprocess.run(['expect', 'konfigurointi.exp', ip_address], check=True)
        print(f"{row['Nimi']} konfigurointi suoritettu osoitteella {ip_address}")
        time.sleep(20)
        subprocess.run(['expect', 'sshtarkistus.exp', ip_address], check=True)
        print(f"{row['Nimi']} ssh tarkistus suoritettu osoitteella {ip_address} ")
        subprocess.run(['expect', 'clusteri.exp', ip_address], check=True)
        print(f"{row['Nimi']} Clusteri suoritettu osoitteella {ip_address}")
