#!/bin/bash

#download images

docker pull albeture/isolgraph:latest
docker pull albeture/ismartcheck:latest
docker pull albeture/icontractlarva:latest
docker pull albeture/isolmet:latest
docker pull albeture/ivandal:latest
docker pull albeture/iethir:latest
docker pull albeture/irattle:latest
docker pull albeture/isecurify:latest
docker pull albeture/imadmax:latest
docker pull albeture/iosiris:latest
docker pull albeture/ioyente:latest

#starting new instance with mongo dependency install

docker run -i --name=vsolgraph -w "/home" -v /outputs:/tmp/outputs albeture/isolgraph bash < mongodb_install.sh
docker run -i --name=vsmartcheck  --volumen-from vsolgraph albeture/ismartcheck bash < mongodb_install.sh
docker run -i --name=vcontractlarva --volumen-from vsolgraph albeture/icontractlarva bash < mongodb_install.sh
docker run -i --name=vsolmet --volumen-from vsolgraph albeture/isolmet bash < mongodb_install.sh
docker run -i --name=vvandal --volumen-from vsolgraph albeture/ivandal bash < mongodb_install.sh
docker run -i --name=vethir --volumen-from vsolgraph albeture/iethir bash < mongodb_install.sh
docker run -i --name=vsecurify --volumen-from vsolgraph albeture/isecurify bash < mongodb_install.sh
docker run -i --name=vmadmax --volumen-from vsolgraph albeture/imadmax bash < mongodb_install.sh
docker run -i --name=vosiris --volumen-from vsolgraph albeture/iosiris bash < mongodb_install.sh
docker run -i --name=voyente -w "/oyente/oyente" --volumen-from vsolgraph albeture/ioyente bash < mongodb_install.sh
