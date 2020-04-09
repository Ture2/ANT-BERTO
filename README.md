# ANT-BERTO

Inside installation folder there are multiples files to make the installation process.
This proyects works with docker and mongodb, so **_it's essential to have installed both tools to following the next steps_**

Install pymongo and docker python libraries into the host.
```
pip install pymongo
pig install docker
```

Pull dockers into host running the following command.
```
./env_docker_install.sh 
```

Launch the mongodb daemon. To generate mongo db just create a database called "ant_berto_db" with mongo interpreter:
```
use ant_berto_db
```
Create mongo collection: 
```
db.createCollection('ethreum_contracts')
```

Repeat the process creating another database called 'store_results' and also a new collection called 'results'
To download full database contract: 'SET LINK HERE'

Import the dataset into our database with the following command:
```
mongoimport --db ant_berto_db --collection contracts --file contratosexport.json
```

Full command list options:

