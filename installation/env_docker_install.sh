#!/bin/bash

#download images

docker pull albeture/isolgraph:latest
docker pull albeture/ismartcheck:latest     modificar la imagen para usar java8 (actualmente usa java 11): https://www.digitalocean.com/community/tutorials/como-instalar-java-con-apt-en-ubuntu-18-04-es
docker pull albeture/icontractlarva:latest
docker pull albeture/isolmet:latest
docker pull mythril/myth
docker pull albeture/ivandal:latest
docker pull albeture/iethir:latest
docker pull albeture/irattle:latest
docker pull albeture/isecurify:latest
docker pull albeture/imadmax:latest
docker pull albeture/iosiris:latest
docker pull albeture/ioyente:latest

#starting new instance with mongo dependency install

docker run -i --name=vsolgraph -w "/home" -v $(pwd)/inputs:/tmp/inputs albeture/isolgraph bash < installation/mongodb_install.sh HECHA
docker run -i --name=vsmartcheck  --volumes-from vsolgraph albeture/ismartcheck bash < installation/mongodb_install.sh HECHA
docker run -i --name=vcontractlarva --volumes-from vsolgraph albeture/icontractlarva bash < installation/mongodb_install.sh NO HACER
docker run -i --name=vsolmet --volumes-from vsolgraph albeture/isolmet bash < installation/mongodb_install.sh HECHA
docker run -i --name=vmythril --volumes-from vsolgraph mythril/myth bash < installation/mongodb_install.sh COMPILADOR
docker run -i --name=vvandal --volumes-from vsolgraph albeture/ivandal bash < installation/mongodb_install.sh HECHA  (FALTA HACER LA LIBRERIA PROPIA DE ANALISIS)
docker run -i --name=vethir --volumes-from vsolgraph albeture/iethir bash < installation/mongodb_install.sh HECHA (FALTA VER UTILIDAD)
docker run -i --name=vsecurify --volumes-from vsolgraph albeture/isecurify bash < installation/mongodb_install.sh COMPILADOR
docker run -i --name=vmadmax --volumes-from vsolgraph albeture/imadmax bash < installation/mongodb_install.sh QUE LIADA
docker run -i --name=vosiris --volumes-from vsolgraph albeture/iosiris bash < installation/mongodb_install.sh HECHA
docker run -i --name=voyente -w "/oyente/oyente" -v $(pwd)/inputs:/tmp/inputs albeture/ioyente bash < installation/mongodb_install.sh HECHA



docker_client.create_container('mythril/myth', command='analyze --solv 0.4.24 /tmp/inputs/input_contract_2.sol', entrypoint='/usr/local/bin/myth', host_config=docker_client.create_host_config(binds=['/Users/Ture/Documents/Blockchain/ANT-BERTO/inputs:/tmp/inputs']))
