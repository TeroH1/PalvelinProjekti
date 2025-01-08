Proxmoxeilla ei ole yhteyttä verkkoon, vain management palvelimeen (debian) -> Asennetaan debianiin apt cacher
sudo apt install apt-cacher-ng

apt cacher ohjeet IP:3142



Proxmoxeille kerrotaan, että niiden pitää käyttää apt cacheria tunnelina. Joko tehdään kaiken kattava proxy tai sitten määritellään tietty repositorio käyttämään managementtiä.
kaiken kattava proxy:
Acquire::http::Proxy "http://192.168.1.1:3142";


Tämä voi esim olla debianilla verkkosivulla tekstinä, koska apache on joka tapauksessa käynnissä. Esim 192.168.1.1/01proxy.txt ja 192.168.1.1/sourceslist.txt (missä on proxmox repo)
curlilla sitten voidaan hakea:

curl 192.168.1.1/sourceslist.txt >> /etc/apt/sources.list
curl 192.168.1.1/01proxy.txt > /etc/apt/apt.conf.d/01proxy
(Voidaan myös appendaa sourceslist jos siel on jotain tärkeetä)

Muista updatee apt proxmoxilla
apt update
tai 
apt dist-upgrade

apt install
Huom. Todennäköisesti FRR:n lataamisen jälkeen tämä kannattaa poistaa. Toinen vaihtoehto on jättää, mutta sitten pitää aina olla management palvelin käytössä.

curl 192.168.1.1/frrconfigfiles/frr-PVE11.conf > /etc/frr/frr.conf

curl 192.168.1.1/interfaceconfigfiles/interface-PVE11.conf >> /etc/network/interfaces




Proxmoxin pitää tehdä (huom nimi muuttuja kahdessa viimesessä):
6 curl 192.168.1.1/sourceslist.txt >> /etc/apt/sources.list
7 curl 192.168.1.1/01proxy.txt > /etc/apt/apt.conf.d/01proxy
8 apt update
9 apt install frr
10 curl 192.168.1.1/frrconfigfiles/frr-PVE$pvenum.conf > /etc/frr/frr.conf
11 curl 192.168.1.1/interfaceconfigfiles/interface-PVE$pvenum.conf >> /etc/network/interfaces
12 systemctl restart frr.service
13 systemctl restart networking.service
