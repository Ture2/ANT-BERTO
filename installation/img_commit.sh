#!/bin/bash

#imagenes: completed

docker commit vsmartcheck ismartcheck
docker commit vsolmet isolmet
docker commit vvandal ivandal
docker commit vethir iethir
docker commit vsecurify isecurify
docker commit vmadmax imadmax
docker commit vosiris iosiris
docker commit vmanticore imanticore
docker commit vslither islither
docker commit vsolgraph isolgraph
docker commit vmythril imythril
docker commit voyente ioyente


docker image tag isolgraph:latest albeture/isolgraph:latest
docker image tag ismartcheck:latest albeture/ismartcheck:latest
docker image tag isolmet:latest albeture/isolmet:latest
docker image tag ivandal:latest albeture/ivandal:latest
docker image tag iethir:latest albeture/iethir:latest
docker image tag isecurify:latest albeture/isecurify:latest
docker image tag imadmax:latest albeture/imadmax:latest
docker image tag iosiris:latest albeture/iosiris:latest
docker image tag ioyente:latest albeture/ioyente:latest
docker image tag imythril:latest albeture/imytrhil:latest
docker image tag islither:latest albeture/islither:latest
docker image tag imanticore:latest albeture/imanticore:latest


docker push albeture/isolgraph:latest
docker push albeture/ismartcheck:latest
docker push albeture/isolmet:latest
docker push albeture/ivandal:latest
docker push albeture/iethir:latest
docker push albeture/isecurify:latest
docker push albeture/imadmax:latest
docker push albeture/iosiris:latest
docker push albeture/ioyente:latest
docker push albeture/imytrhil:latest
docker push albeture/islither:latest
docker push albeture/imanticore:latest



#Starting enviroment from here

docker pull albeture/isolgraph:latest
docker pull albeture/ismartcheck:latest
docker pull albeture/isolmet:latest
docker pull albeture/ivandal:latest
docker pull albeture/iethir:latest
docker pull albeture/isecurify:latest
docker pull albeture/imadmax:latest
docker pull albeture/iosiris:latest
docker pull albeture/ioyente:latest
docker pull albeture/imytrhil:latest
docker pull albeture/islither:latest
docker pull albeture/imanticore:latest

#añadir dependencias mongo: 




#docker run -it --name=<nombre contenedor> -v /test/:/tmp/test <nombre imagen>
#docker run -it --name=<nombre otro contenedor> --volumen-from <contenedor con el volumen> <nombre otra imagen>


docker run -i --name=vsolgraph -w "/home" -v /outputs:/tmp/outputs isolgraph bash < mongodb_install.sh
docker run -i --name=vsmartcheck  --volumen-from vsolgraph ismartcheck bash < mongodb_install.sh
docker run -i --name=vcontractlarva --volumen-from vsolgraph icontractlarva bash < mongodb_install.sh
docker run -i --name=vsolmet --volumen-from vsolgraph isolmet bash < mongodb_install.sh
docker run -i --name=vvandal --volumen-from vsolgraph ivandal bash < mongodb_install.sh
docker run -i --name=vethir --volumen-from vsolgraph iethir bash < mongodb_install.sh
docker run -i --name=vsecurify --volumen-from vsolgraph isecurify bash < mongodb_install.sh
docker run -i --name=vmadmax --volumen-from vsolgraph imadmax bash < mongodb_install.sh
docker run -i --name=vosiris --volumen-from vsolgraph iosiris bash < mongodb_install.sh
docker run -i --name=voyente --volumen-from vsolgraph ioyente bash < mongodb_install.sh
