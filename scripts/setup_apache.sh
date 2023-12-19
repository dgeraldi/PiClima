#!/bin/bash

#Inclui usuario para editar conteudo no apache
#sudo usermod -a -G www-data daniel
#sudo chown -R -f www-data:www-data /var/www/html

#Instala o php
#sudo apt-get install php8.0

#Move conteudo apos clone do github para /var/www/html
echo 'Movendo localweb/ para /var/www/html/PiClima'
sudo mv /home/pi/PiClima/PiClima/localweb /var/www/html/PiClima