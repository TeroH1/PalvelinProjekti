#!/usr/bin/env bash
apt update
#apt install git
#git clone https://github.com/TeroH1/PalvelinProjekti
apt install isc-dhcp-server
nano /etc/default/isc-dhcp-server
apt install tftp-server
mkdir /srv/tftp/PVEXXX
systemctl start tftpd-hpa.service
apt install pxelinux
cp /usr/lib/PXELINUX/lpxelinux.0 /srv/tftp/PVEXXX/lpxelinux.0 
cp /lib/syslinux/modules/bios/ldlinux.c32 /srv/tftp/PVEXXX/ldlinux.c32
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
chmod 777 /var/www/html/PVEXXX/answer.toml
apt install gh
apt install expect
apt install apt-cacher-ng
systemctl start apt-cacher-ng
sh -c 'echo "Acquire::http::Proxy \"http://192.168.1.1:3142\";" > /etc/apt/apt.conf.d/01proxy'
cp /etc/apt/sources.list /var/www/html/sourceslist.txt
cp /etc/apt/apt.conf.d/01proxy /var/www/html/01proxy.txt
apt-get install frr -y
mkdir /var/www/html/frrconfigfiles/
mkdir /var/www/html/interfaceconfigfiles/
wget "https://enterprise.proxmox.com/iso/proxmox-ve_8.3-1.iso" -O "proxmox-ve_8.3-1.iso"
mkdir -p /mnt/proxmox
mount -o loop proxmox-ve_8.3-1.iso /mnt/proxmox
cp "/mnt/proxmox/boot/linux26" "/srv/tftp/PVEXXX"
cp "/mnt/proxmox/boot/initrd.img" .
umount /mnt/proxmox
rmdir /mnt/proxmox
proxmox-auto-install-assistant prepare-iso proxmox-ve_8.3-1.iso --fetch-from http --url http://192.168.1.1/PVEXXX/answer.toml
chmod 777 proxmox-ve_8.3-1-auto-from-http-url.iso
zstd -d initrd.img -o initrdkansio
cpio -idmv -D uusini < initrdkansio
mv "proxmox-ve_8.3-1-auto-from-http-url.iso"  "proxmox.iso"
cp "proxmox.iso" "uusini/"
(
  cd "uusini"
  find . | cpio -H newc -o > ../initrduusi
)
gzip -9 -S ".img" initrduusi
mv initrduusi.img "/var/www/html/PVEXXX/initrd.img"
rm -r uusini
rm -r initrd.img
rm -r proxmox.iso
rm -r proxmox-ve_8.3-1.iso 
rm -r initrdkansio 
rm -r auto-installer-mode.toml 
systemctl restart apt-cacher-ng.service
