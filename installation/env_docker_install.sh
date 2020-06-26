#!/bin/bash

#download images

docker pull albeture/isolgraph:latest
docker pull albeture/ismartcheck:latest
docker pull albeture/icontractlarva:latest
docker pull albeture/isolmet:latest
docker pull albeture/imythril:latest
docker pull albeture/ivandal:latest
docker pull albeture/iethir:latest
docker pull albeture/irattle:latest
docker pull albeture/isecurify:latest
docker pull albeture/imadmax:latest
docker pull albeture/iosiris:latest
docker pull albeture/ioyente:latest

#starting new instance with mongo dependency install

docker run -i --name=vsolgraph -w "/home" -v $(pwd)/inputs:/tmp/inputs albeture/isolgraph
docker run -i --name=vsmartcheck  --volumes-from vsolgraph albeture/ismartcheck
docker run -i --name=vmanticore --volumes-from vsolgraph albeture/imanticore
docker run -i --name=vsolmet --volumes-from vsolgraph albeture/isolmet
docker run -i --name=vmythril --volumes-from vsolgraph albeture/imythril
docker run -i --name=vvandal --volumes-from vsolgraph albeture/ivandal
docker run -i --name=vethir --volumes-from vsolgraph albeture/iethir
docker run -i --name=vsecurify --volumes-from vsolgraph albeture/isecurify
docker run -i --name=vmadmax --volumes-from vsolgraph albeture/imadmax
docker run -i --name=vosiris --volumes-from vsolgraph albeture/iosiris
docker run -i --name=voyente --volumes-from vsolgraph albeture/ioyente
docker run -i --name=vslither --volumes-from vsolgraph albeture/islither 
