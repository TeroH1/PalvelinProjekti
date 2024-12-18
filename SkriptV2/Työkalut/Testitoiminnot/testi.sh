#!/bin/sh
sudo systemctl status apache2 --no-pager
sudo systemctl status isc-dhcp-server --no-pager
sudo systemctl status tftpd-hpa.service --no-pager

