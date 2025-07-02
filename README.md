🚀🚀Proxmox palvelimen automatisoinnin skriptitiedostot🚀🚀


Projektin tavoite on automatisoida Proxmox palvelimen asennus ja konfigurointi käyttäen apuna etenkin PXE:tä ja expect-ohjelmaa.
Skripti on tuotettu spesifisesti juuri projektin kohteena olevaan ympäristöön, mutta on helposti mukautettavissa mihin tahansa Proxmox ympäristöön. 
konfigurointi.exp ja clusteri.exp tarkoitus on etenkin testata/osoittaa miten eri komentojen ajo automatisoidusti onnistuu.
Työkalu ASENNA_KAIKKI.sh asentaa tarvittavat paketit tyhjälle virtuaalikoneelle (Debian) ja luo aloitukseen tarvittavat tiedostot (ks. example of use)
Skriptin suorittaessa eri palvelimien expect-skriptien tulosteet ohjautuvat Logit-kansioon.


Automaattisen asennuksen kulkukaavio esitetään alla olevassa kuvassa. Lähtökohta kuvan alkutilanteeseen on se, että tarvittavat asennukset on tehty virtuaalikoneelle ASENNA_KAIKKI.sh skriptin mukaisesti.

![kuva](https://github.com/user-attachments/assets/fddacd57-747c-4083-a944-1f378f9338c7)



Example of use:
1. Lataa Debian (testattu v12.9)
2. Asenna tarvittavat paketit ja luo tarvittavat tiedostot käyttäen /SkriptV2/Työkalut/ASENNA_KAIKKI.sh (huom ajettava sudoerina)
   Huom. Skripti haluaa käyttäjän määrittävän DHCP:ssä käytettävän interfacen IPv4 = "" kohtaan. Lisää se ja poistu nanosta (save n quit) 
3. (optional) Suorita python ohjelma /SkriptV2/Työkalut/MAC-sniffer/MAC-sniffer.py
4. (optional) Käynnistä asennettava palvelin niin, että se yrittää hakea PXE bootilla DHCP-osoitetta
   MAC-sniffer kysyy tarvittavat tiedot
5. (optional) Ota tarvittavat tiedot luodusta tiedostosta mac-osoitteet.csv
6. Kirjoita/kopioi tiedostoon SkriptV2/Tiedot.csv tarvittavat tiedot ja otsikot:
  'Nimi', 'MAC-osoite', 'PVEn-ip', 'Loopback', 'PrimaryLink-ip', 'SecondaryLink-ip', 'Subnet', 'PrimaryLink-naapuri', 'SecondaryLink-naapuri', 'Konfiguroitu'
   Esimerkki:


   Nimi  |	MAC-osoite        |	PVEn-ip      |	Loopback  |	PrimaryLink-ip|	SecondaryLink-ip|	Subnet|	PrimaryLink-naapuri  |	SecondaryLink-naapuri  |	Konfiguroitu|

   
   pve11 |	00:0c:29:80:69:7e |	192.168.1.11 |	10.5.1.48 |	10.15.1.96    |	10.15.2.96      |	31    |	10.15.1.96           |	10.15.2.96             |	False       |

8. Suorita python /SkriptV2/automatisointiscripti.py
9. Seuraa asennuksen etenemistä /SkriptV2/Logit/ kansiosta
