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
				fieldnames = ['Nimi', 'MAC-osoite', 'Loopback', 'Link-ip/subnet', 'Link-naapuri', 'Konfiguroitu']
				writer = csv.DictWriter(file, fieldnames=fieldnames)
				writer.writeheader() 
				writer.writerows(rows)  
				print(rows) # Debug printti

def palvelinkonffit(nimi, loopback, linkip, neighborip):
	global interfaces_config
	global frr_config
	interfaces_config = f"""#/etc/network/intefaces
auto eno1
	iface eno1 inet static
	address 10.10.1.{linkip}        
	mtu 9216
	#TO_FABRIB_L2A_ETH1
	
auto eno2
	iface eno2 inet static
	address 10.10.2.{linkip}
	mtu 9216
	#TO_FABRIC_L2B_ETH1
	
auto enroute0
	iface enroute0 inet static
	address {loopback}/32
	mtu 9216
	pre-up ip link add enroute0 type dummy

auto VLAB_SAN
	iface VLAB_SAN inet manual
	address 192.168.7.240/24
	bridge-ports none
	bridge-stp off
	bridge-fd 0
	
auto vxlan7001
	iface vxlan7001 inet manual
	pre-up ip link add vxlan7001 type vxlan id 7001 dstport 4789 local 10.2.1.{loopback} nolearning
	pre-up ip link set dev vxlan7001 master VLAB_SAN
	pre-up ip link set up dev vxlan7001
	post-up ip link set mtu 9000 dev vxlan7001"""
	
	frr_config = f"""!
frr version 8.5.2
frr defaults datacenter
hostname test
log syslog informational
no ip forwarding
no ipv6 forwarding
service integrated-vtysh-config
!
router bgp 65002
bgp router-id {loopback}
bgp graceful-restart-disable
neighbor LEAF peer-group
neighbor LEAF remote-as 65001
neighbor LEAF capability dynamic
neighbor 10.10.1.{neighborip} peer-group LEAF
neighbor 10.10.2.{neighborip} peer-group LEAF
bgp allow-martian-nexthop
!
address-family ipv4 unicast
  network {loopback}/32
  neighbor LEAF allowas-in
  maximum-paths 8
exit-address-family
!
address-family l2vpn evpn
  neighbor LEAF activate
  neighbor LEAF allowas-in
  advertise-all-vni
  advertise-svi-ip
  advertise ipv4 unicast
exit-address-family
exit
end"""
	lista.append(frr_config)
	lista.append(interfaces_config)

input_file = 'Tiedot.csv'
output_file = 'Tiedot.csv'

with open(input_file, mode='r', newline='') as file:
    reader = csv.DictReader(file)
    rows = []
    for row in reader:
        lista = []		
        nimi = row['Nimi']
        loopback = row['Loopback']
        linkip = row['Link-ip/subnet']
        neighborip = row['Link-naapuri']
        
        frrkonfigfile = f'/var/www/html/frrconfigfiles/frr-{nimi}.conf'
        interfacekonfigfile = f"/var/www/html/interfaceconfigfiles/interface-{nimi}.conf"
               
        palvelinkonffit(nimi, loopback, linkip, neighborip)
        print(lista[0])
        print(lista[1])
        
        with open(frrkonfigfile, mode='w') as file:
            file.write(frr_config)
        with open(interfacekonfigfile, mode='w+') as file:
            file.write(interfaces_config)
            
        
        

input_file = 'Tiedot.csv'
output_file = 'Tiedot.csv'
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
	
