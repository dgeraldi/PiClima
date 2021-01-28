# ***PiClima***

![GitHub](https://img.shields.io/github/license/dgeraldi/PiClima?style=plastic)  ![GitHub last commit](https://img.shields.io/github/last-commit/dgeraldi/PiClima?style=plastic)

## ***1 OBJETIVO***

Este projeto visa capturar dados de sensores ligados a um raspberry pi e armazenamento em bases de dados para consulta online via frontend.

## ***2 ARQUITETURA***

Arquitetura (alto nível)

![alt text](https://github.com/dgeraldi/PiClima/blob/main/Files/PiClima.png)

## ***3 INSTALAÇÃO***

### ***3.1 Pre-Requisitos***

![npm](https://img.shields.io/npm/v/npm?style=plastic)

Software:

* Python 3.9
  * mysqlclient
  * pymongo
  * dnspython
  * spidev
  * Adafruit Python BMP180
* MySQL
  
Hardware:

* Raspberry Pi (aqui na versão 3) com Raspbian (não testado com versões recentos do SO)
* Sensor de Pressão Barométrica BMP180

  
#### 3.1.1 OpenSSL > v1.1.0 (Opcional), apenas caso ocorra um erro de SSL ao utilizar o pip

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


#### 3.1.2 Python 3.9

Para este projeto utilizei o python3.9 para coleta dos dados dos sensores, para sua instalação pode-se utilizar o bom e velho ```sudo apt-get install python3.9``` após adicionar seu correto ppa ou compilando e instalando conforme a seguir (para meu caso, devido ao erro do ssl optei por compilar). 

```console
#Download da versão desejada
foo@bar:~$ wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tar.xz
foo@bar:~$ tar -xvf Python-3.9.0.tar.xz
foo@bar:~$ cd Python-3.0.0

#Configure passando o openssl como parâmetro
foo@bar:~$ ./configure --with-openssl=/usr/local/openssl --enable-optimizations
foo@bar:~$ make
foo@bar:~$ make install

foo@bar:~$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.4 0
foo@bar:~$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
```


#### 3.1.3 Dependencias Específicas

Algumas das dependências necessárias para o script rodar corretamente:

1. Mysqlclient, pymongo, spidev e dnspython
Necessário para conectar com o mysql, mongoDB na nuvem

```console
foo@bar:~$ sudo pip3 install mysqlclient pymongo dnspython spidev
```
2. Adafruit BMP180 Python
Biblioteca necessária para coletar os dados através do sensor BMP180

```console
foo@bar:~$ git clone https://github.com/adafruit/Adafruit_Python_BMP.git
foo@bar:~$ cd Adafruit_Python_BMP
foo@bar:~$ sudo python3 setup.py install
```


### ***3.2 Banco de Dados***

#### 3.2.1 Banco de Dados MySQL

Database: tempodg
Table: log_temperatura

| COLUMN_NAME    | COLUMN_TYPE  | COLUMN_KEY | EXTRA          |
|----------------|--------------|------------|----------------|
| codTemperatura | int(11)      | PRI        | auto_increment |
| dataLog        | timestamp    |            |                |
| temperatura    | decimal(4,2) |            |                |
| pressao        | decimal(7,2) |            |                |
| altitude       | int(4)       |            |                |
| pressao_abs    | decimal(7,2) |            |                |


#### 3.2.2 Banco de dados MongoDB

Database: weather_dg
Collection: log_temperatura

| COLUMN     |
|------------|
| _id: index |
| datahora   |
| temperatura|
| pressao    |
| pressao_abs|
| altitude   |

## ***Checklist - Macro***

- [X] Criar bancos: local mysql e mongodb (utilizando serviço cloud Mongo Atlas);
- [X] Criar script python raspberry pi para coleta de dados e envio aos BD;
- [ ] Criar página web interna (php) com gráficos para uso rede interna (redundância visto quedas de internet constantes devido nossas ótimas operadoras);
- [ ] Criar página web em node.js para consulta online via internet;
- [ ] Criar APIs para consulta de dados;
- [ ] Criar mecanismo para caso de falha no upload no mongoDB na nuvem, poder enviar os dados posteriormente represados;
