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

<<<<<<< HEAD
docker run -i --name=vsolgraph -w "/home" -v $(pwd)/inputs:/tmp/inputs albeture/isolgraph bash < installation/mongodb_install.sh
docker run -i --name=vsmartcheck  --volumes-from vsolgraph albeture/ismartcheck bash < installation/mongodb_install.sh
docker run -i --name=vcontractlarva --volumes-from vsolgraph albeture/icontractlarva bash < installation/mongodb_install.sh
docker run -i --name=vsolmet --volumes-from vsolgraph albeture/isolmet bash < installation/mongodb_install.sh
docker run -i --name=vvandal --volumes-from vsolgraph albeture/ivandal bash < installation/mongodb_install.sh
docker run -i --name=vethir --volumes-from vsolgraph albeture/iethir bash < installation/mongodb_install.sh
docker run -i --name=vsecurify --volumes-from vsolgraph albeture/isecurify bash < installation/mongodb_install.sh
docker run -i --name=vmadmax --volumes-from vsolgraph albeture/imadmax bash < installation/mongodb_install.sh
docker run -i --name=vosiris --volumes-from vsolgraph albeture/iosiris bash < installation/mongodb_install.sh
docker run -i --name=voyente -w "/oyente/oyente" -v $(pwd)/inputs:/tmp/inputs albeture/ioyente bash < installation/mongodb_install.sh
=======
docker run -i --name=vsolgraph -w "/home" -v ($pwd)/outputs:/tmp/outputs albeture/isolgraph bash < mongodb_install.sh
docker run -i --name=vsmartcheck  --volumes-from vsolgraph albeture/ismartcheck bash < mongodb_install.sh
docker run -i --name=vcontractlarva --volumes-from vsolgraph albeture/icontractlarva bash < mongodb_install.sh
docker run -i --name=vsolmet --volumes-from vsolgraph albeture/isolmet bash < mongodb_install.sh
docker run -i --name=vvandal --volumes-from vsolgraph albeture/ivandal bash < mongodb_install.sh
docker run -i --name=vethir --volumes-from vsolgraph albeture/iethir bash < mongodb_install.sh
docker run -i --name=vsecurify --volumes-from vsolgraph albeture/isecurify bash < mongodb_install.sh
docker run -i --name=vmadmax --volumes-from vsolgraph albeture/imadmax bash < mongodb_install.sh
docker run -i --name=vosiris --volumes-from vsolgraph albeture/iosiris bash < mongodb_install.sh
docker run -i --name=voyente -w "/oyente/oyente" --volumes-from vsolgraph albeture/ioyente bash < mongodb_install.sh
>>>>>>> parent of 723aaa0... v0.2 Solgraph and Oyente works correctly, refactored code
