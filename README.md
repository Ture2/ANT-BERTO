# ANT-BERTO

Inside installation folder there are multiples files to make the installation process.
This proyects works with docker and mongodb, so **_it's essential to have installed both tools to following the next steps_**

Then run:
```
./env_docker_install.sh 
```
To pull the differents tool docker images.

Launch the mongodb daemon. To generate mongo db just create a database called "mydb" and into it a collection called "contratos"
```
use mydb
mydb.collection.insertOne( { x: 1 } );
```

You can find the ethereum database contract here: 

Import the database with the following command:
```
mongoimport --db my --collection contratos --file contratosexport.json
```
