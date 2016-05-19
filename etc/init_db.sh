#!/usr/bin/env bash
sudo /etc/init.d/mysql restart
mysql -uroot -e "CREATE DATABASE STEPIC_WEB_TECH;"
mysql -uroot -e "CREATE USER 'STEPIC'@'localhost' IDENTIFIED BY 'STEPIC';"
mysql -uroot -e "GRANT ALL PRIVILEGES ON * . * TO 'STEPIC'@'localhost';"
mysql -uroot -e "FLUSH PRIVILEGES;"
