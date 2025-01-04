apt install isc-dhcp-server
nano /etc/default/isc-dhcp-server
apt install tftp-server
mkdir /srv/tftp/PVEXXX
systemctl start tftpd-hpa.service
apt install pxelinux
cp /usr/lib/PXELINUX/lpxelinux.0 /srv/tftp/PVEXXX/lpxelinux.0 
mkdir /srv/tftp/PVEXXX/pxelinux.cfg/
echo 'DEFAULT install 
LABEL install 
        MENU LABEL Install Proxmox VE 
        linux linux26  
        INITRD http://192.168.1.1/PVEXXX/initrd.img 
        APPEND proxmox-start-auto-installer' > /srv/tftp/PVEXXX/pxelinux.cfg/default
apt install apache2
mkdir /var/www/html/PVEXXX
mkdir /home/autoinstallerfiles
systemctl restart apache2
echo 'deb [trusted=yes] http://download.proxmox.com/debian/pve bookworm pve-no-subscription' >> /etc/apt/sources.list
apt update
apt install proxmox-auto-install-assistant
echo 'mode = "http" 
[http] 
url = http://192.168.1.1/PVEXXX/answer.toml' > /home/autoinstallerfiles/auto-installer-mode.toml
echo "[global] 
keyboard = "fi" 
country = "at" 
fqdn = "pvexxx.testinstall" 
mailto = "mail@no.invalid" 
timezone = "Europe/Vienna" 
root_password = "123456" 

[network] 
source = "from-dhcp" 

[disk-setup] 
filesystem = "ext4" 
lvm.swapsize = 0 
lvm.maxvz = 0 
disk_list = ['sda']" > /var/www/html/PVEXXX/answer.toml
apt install gh
apt install git
apt install expect
