# ***PiClima***
![image](https://user-images.githubusercontent.com/77708243/131872337-883f6ac5-8b04-41ee-9f14-99911d1daf91.png)

![GitHub](https://img.shields.io/github/license/dgeraldi/PiClima?style=plastic)  ![GitHub last commit](https://img.shields.io/github/last-commit/dgeraldi/PiClima?style=plastic)


Tabela de conteúdos
=================
  * [1 Objetivo](#objective)
  * [2 Arquitetura](#arch)
  * [3 Instalação](#install)
    + [3.1 Pre-Requisitos](#prereqs)
      - [3.1.1 Hardware](#hardware)
      - [3.1.2 Dependencias](#dependencies)
    + [3.2 Banco de Dados](#databases)
      - [3.2.1 MySQL](#mysql)
      - [3.2.2 MongoDB](#mongodb)
  * [4 Como Usar](#howtouse)
    + [4.1 Resultado PHP](#phpresults)
  * [5 Solução de Problemas](#problemssolutions)


## ***1 OBJETIVO***<a name="objective"></a>

Este projeto visa capturar dados de sensores ligados a um raspberry pi e armazenamento em bases de dados para consulta online via frontend.


## ***2 ARQUITETURA***<a name="arch"></a>

Arquitetura lógica

![alt text](https://github.com/dgeraldi/PiClima/blob/main/Files/PiClima_v2.png)

Conexão física

![alt text](https://github.com/dgeraldi/PiClima/blob/main/Files/PiClima%20Schematic/Schematic_Raspberry%20Pi_2023-11-20.png)

## ***3 INSTALAÇÃO***<a name="install"></a>

### ***3.1 Pre-Requisitos***<a name="prereqs"></a>

![npm](https://img.shields.io/npm/v/npm?style=plastic)
  
  
#### 3.1.1 Hardware<a name="hardware"></a>

* Raspberry Pi (aqui na versão 3) com Raspbian (não testado com outras versões)
* Sensor de Pressão Barométrica BMP180
* Sensor de Umidade e Temperatura DHT11, DHT22 ou AHT10


#### 3.1.2 Dependencias<a name="dependencies"></a>

Algumas das dependências necessárias para o script rodar corretamente:

* PHP
* Python
  * Python 3.9
  * mysqlclient
  * python-decouple
  * pymongo
  * dnspython
  * Adafruit Python BMP180
  * Adafruit Python DHT
  * SMBUS (para AHT10 - sem biblioteca necessária)
  * Colorama - For pretty console prints
* Composer
* I2C habilitado
* MySQL

a. Python 3.9

Para este projeto utilizei o python3.9 para coleta dos dados dos sensores, para sua instalação pode-se utilizar ```sudo apt-get install python3.9``` após adicionar seu correto PPA ou compilando e instalando conforme a seguir. 

```console
#Download da versão desejada
foo@bar:~$ wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz
foo@bar:~$ tar -xvf Python-3.9.0.tar.xz
foo@bar:~$ cd Python-3.9.0

#Configure passando o openssl como parâmetro
foo@bar:~$ ./configure --with-openssl=/usr/local/openssl --enable-optimizations
foo@bar:~$ make
foo@bar:~$ make install

foo@bar:~$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.4 0
foo@bar:~$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
```

b. Mysqlclient, Python-Decouple, pymongo e dnspython
Necessário para conectar com o mysql local e mongoDB na nuvem

```console
foo@bar:~$ sudo pip3 install mysqlclient python-decouple pymongo dnspython
```

c. Composer
Gerenciador de dependências para PHP, utilizado para a dependência vlucas/phpdotenv que possibilita captura de variáveis em arquivo de ambiente (.env).

```console
foo@bar:~$ php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
foo@bar:~$ php -r "if (hash_file('sha384', 'composer-setup.php') === 'e21205b207c3ff031906575712edab6f13eb0b361f2085f1f1237b7126d785e826a450292b6cfd1d64d92e6563bbde02') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
foo@bar:~$ php composer-setup.php
foo@bar:~$ php -r "unlink('composer-setup.php');"
foo@bar:~$ sudo mv composer.phar /usr/local/bin/composer
```

Instalar as dependências existentes no arquivo composer.json

```console
foo@bar:~$ composer install
```

Ou

```console
foo@bar:~$ composer require vlucas/phpdotenv
```

d. Adafruit BMP180 Python
Biblioteca necessária para coletar os dados através do sensor BMP180

```console
foo@bar:~$ git clone https://github.com/adafruit/Adafruit_Python_BMP.git
foo@bar:~$ cd Adafruit_Python_BMP
foo@bar:~$ sudo python3 setup.py install
```

e. Adafruit DHT Python
Biblioteca necessária para coletar dados de umidade e temperatura através do sensor DHT11 ou DHT22
```console
foo@bar:~$ git clone https://github.com/adafruit/Adafruit_Python_DHT.git
foo@bar:~$ cd Adafruit_Python_DHT
foo@bar:~$ sudo python3 setup.py install
```

f. Habilitar interface I2C
Digitar no console
```console
foo@bar:~$ sudo raspi-config
```

Selecionar no menu Interface Options->I2C e habilitar a opção.


### ***3.2 Banco de Dados***<a name="databases"></a>

#### 3.2.1 Banco de Dados MySQL<a name="mysql"></a>

Após instalado o mysql/mariadb, faz-se necessário criar o database e a tabela conforme esquema a seguir

a. Criar database
Escolha o nome que desejar e atulize o arquivo /sensors/.env

```sql
create database tempodg;
```

b. Criar tabela
Utilize o nome da tabela que desejar e atualize o arquivo /sensors/.env conforme novos nomes.

```sql 
CREATE TABLE `log_temperatura` ( `id` int(11) NOT NULL AUTO_INCREMENT,  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,  `press_temperature` decimal(4,2) NOT NULL,  `pressure` decimal(7,2) NOT NULL, `altitude` int(4) NOT NULL, `pressure_abs` decimal(7,2) NOT NULL, `humidity` decimal(4,2) NOT NULL, `hum_temperature` decimal(4,2) NOT NULL,`heat_index` decimal(4,2) NOT NULL, PRIMARY KEY (`id`)) ENGINE=MyISAM DEFAULT CHARSET=latin1;
```

Database: tempodg
Table: log_temperatura

| COLUMN_NAME          | COLUMN_TYPE  | COLUMN_KEY | EXTRA          |
|----------------------|--------------|------------|----------------|
| id                   | int(11)      | PK         | auto_increment |
| created              | timestamp    |            |                |
| press_temperature    | decimal(4,2) |            |                |
| pressure             | decimal(7,2) |            |                |
| altitude             | int(4)       |            |                |
| pressure_abs         | decimal(7,2) |            |                |
| humidity             | decimal(4,2) |            |                |
| hum_temperature      | decimal(4,2) |            |                |
| heat_index           | decimal(4,2) |            |                |


c. Criar um usuário no mysql
```sql 
CREATE USER 'USUARIO'@'localhost' IDENTIFIED BY 'SENHA';
```

d. Garantir acesso ao banco
```sql 
GRANT ALL PRIVILEGES ON tempodg.* TO 'USUARIO'@'localhost';
```


#### 3.2.2 Banco de dados MongoDB<a name="mongodb"></a>

Para os serviços de banco de dados MONGO foi utilizado o MONGODB ATLAS.

Database: weather_dg (Atualizar no script posteriormente com o novo nome)
Collection: log_temperatura (Atualizar no script com o novo nome)

| COLUMN                |
|-----------------------|
| _id: index            |
| created               |
| press_temperature     |
| pressure              |
| pressure_abs          |
| altitude              |
| humidity              |
| hum_temperature       |
| heat_index            |


## ***4 COMO USAR***<a name="howtouse"></a>

* Copie o repositório com os scripts para o raspberry pi e crie um arquivo no diretório /sensors/ chamado .env com o seguinte conteúdo:

```
#*******************
#Database SQL
SQLSERVER=localhost
SQLDBNAME=dbName
SQLTABLENAME=tableName
USER_SQL=usrName
SECRET_SQL=passwordSQL

#*******************
#Database Mongo
SEND_TO_MONGO=false
USER_MONGO=usrName
SECRET_MONGO=passwordMongo
MONGO_DBNAME=weather_dg
MONGO_COLLECTIONNAME=log_weather

#*******************
#Activate sensors setting true or false (lower case)
#Pressure - BMP180
PRESSURE=true
#Local altitute to compensate pressure from sea level
LOCAL_ALTITUDE=470

#Humidity - DHT11 or AHT10
HUMIDITY=true
#Use which sensor
DHT_SENSOR=false
AHT_SENSOR=true

#When not using I2C, like in DHT11, uncomment the line below to set data pin on raspberry
HUMIDITY_PIN=24
```

* Para executar basta digitar o comando ```python3 main.py``` no terminal.

* Para realizar coleta de forma automática em períodos específicos, basta realizar o agendamento para execução automática utilizando o crontab.

No terminal digite:

```console
foo@bar:~$ crontab -e
```

E insira a seguinte linha no final do arquivo para agendar a execução a cada 30 minutos o script localizado no diretorio home

```console
*/30 * * * * python3 ~/main.py
```

* Mova o conteúdo do diretório ```/localweb/*``` para o diretório do apache nomeando sua página ```/var/www/html/PiClima```

Para visualizar seus dados, digite no browser http://localhost/PiClima/temp.php


### ***4.1 Resultado PHP***<a name="phpresults"></a>

![image](https://github.com/dgeraldi/PiClima/blob/main/Files/PiClima%20Homepage.png)

## ***5 SOLUÇÃO DE PROBLEMAS***<a name="problemssolutions"></a>

## ***5.1 OpenSSL > v1.1.0 (Opcional, apenas caso ocorra um erro de SSL ao utilizar o pip)

Ao instalar alguma dependência do python via pip o erro abaixo é retornado impedindo a correta instalação.

```console
pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
Collecting mysqlclient
  Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/mysqlclient/
  Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/mysqlclient/
 [...]
  Could not fetch URL https://pypi.org/simple/numpy/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host='pypi.org', port=443): Max retries exceeded with url: /simple/numpy/ (Caused by SSLError("Can't connect to HTTPS URL because the SSL module is not available.")) - skipping
  Could not find a version that satisfies the requirement numpy (from versions: )
No matching distribution found for numpy
pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
Could not fetch URL https://pypi.org/simple/pip/: There was a problem confirming the ssl certificate: HTTPSConnectionPool(host='pypi.org', port=443): Max retries exceeded with url: /simple/pip/ (Caused by SSLError("Can't connect to HTTPS URL because the SSL module is not available.")) - skipping
```

Para resolver definitivamente faz-se necessário a instalação ou upgrade do openssl para versão > 1.1.0 e a reinstalação do python3.9 passando como parametros o uso do novo openssl, para isso:

```console
#checa versão atual
foo@bar:~$ openssl version

#baixa o openssl
foo@bar:~$ sudo wget https://www.openssl.org/source/openssl-1.0.2o.tar.gz

#Descompacta e entramos no diretório
foo@bar:~$ tar -zxvf openssl-1.1.1i.tar.gz 
foo@bar:~$ cd openssl-1.1.1i/

#configuramos e instalamos
foo@bar:~$ ./config --prefix=/usr/local/openssl shared no-zlib
foo@bar:~$ make
foo@bar:~$ make install

#muda-se as configurações atuais
foo@bar:~$ ln -s /usr/local/openssl/include/openssl /usr/include/openssl
foo@bar:~$ ln -s /usr/local/openssl/lib/libssl.so.1.1 /usr/local/lib/libssl.so
foo@bar:~$ ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl
foo@bar:~$ echo "/usr/local/openssl/lib" >> /etc/ld.so.conf

#checa a versão final
foo@bar:~$ openssl version
```
