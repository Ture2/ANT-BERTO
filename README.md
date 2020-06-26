# ANT-BERTO

Inside installation folder there are multiples files to make the installation process.
This proyects works with docker and mongodb, so **_it's essential to have installed both tools to following the next steps_**

Install pymongo and docker python libraries into the host.
```
pip install pymongo
pip install docker

```

Pull and set up dockers into host running the following command.
```
./env_docker_install.sh 
```

Launch the mongodb daemon. To generate mongo db just create a database called "mydb" (for contracts) with mongo interpreter:
```
use mydb
```
Create mongo collection: 
```
db.createCollection('contratos_full')
```
And repeats the two previous steps creating a new database called "results_db" and a new collection inside called "outputs_full":

```
use mydb
db.createCollection('outputs_full')
```
Technically, you could use whatever name you want. The tool currently is working with those names but in constants file you could set up any name you want.

To download full database contract: 'SET LINK HERE'

Import the dataset into our database with the following command:
```
mongoimport --db mydb --collection contratos_full --file contratosexport.json
```
Then you could run the tool.
If you see some pip package that is not installed, just install it with pip an try again.
