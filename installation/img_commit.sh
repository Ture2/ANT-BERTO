#!/bin/bash

#imagenes: completed

docker commit solgraph isolgraph
docker commit smartcheck ismartcheck
docker commit contractlarva icontractlarva
docker commit solmet isolmet
docker commit vandal ivandal
docker commit ethir iethir
docker commit rattle irattle
docker commit securify isecurify
docker commit madmax imadmax
docker commit youthful_chatterjee iosiris
docker commit frosty_booth ioyente

docker image tag isolgraph:latest albeture/isolgraph:latest
docker image tag ismartcheck:latest albeture/ismartcheck:latest
docker image tag icontractlarva:latest albeture/icontractlarva:latest
docker image tag isolmet:latest albeture/isolmet:latest
docker image tag ivandal:latest albeture/ivandal:latest
docker image tag iethir:latest albeture/iethir:latest
docker image tag irattle:latest albeture/irattle:latest
docker image tag isecurify:latest albeture/isecurify:latest
docker image tag imadmax:latest albeture/imadmax:latest
docker image tag iosiris:latest albeture/iosiris:latest
docker image tag ioyente:latest albeture/ioyente:latest

#Starting enviroment from here

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

docker start vsolgraph
docker start vsmartcheck
docker start vcontractlarva
docker start vsolmet
docker start vvandal
docker start vethir
docker start vsecurify
docker start vmadmax
docker start vosiris
docker start voyente

#ejecutar los test en cada herramienta redirigiendo la entrada


#guardar los resultados dentro del volumen comun 

#sacar esos datos al host maestro o analizador

	#analizador en python

#devolver un único archivo