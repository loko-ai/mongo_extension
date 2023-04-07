<html><p><a href="https://loko-ai.com/" target="_blank" rel="noopener"> <img style="vertical-align: middle;" src="https://user-images.githubusercontent.com/30443495/196493267-c328669c-10af-4670-bbfa-e3029e7fb874.png" width="8%" align="left" /> </a></p>
<h1>Mongo extension</h1><br></html>


 **Mongo extension** is a Loko extension dealing with MongoDB connection.

It allows to insert, query, delete data and list your collections directly within the workflows using the **MongoDB** 
component or to display the DB content from the **db manager** GUI.
<p align="center"><img src="https://user-images.githubusercontent.com/30443495/230626093-6aafa47c-b083-4207-a935-58a7d017be11.png" width="80%" /></p>

## Configuration

In the file *config.json* you can configure your MongoDB connection: 

```
{
  "main": {
    "environment": {
      "HOST": "mongo_extension_mongo",
      "PORT": "27017",
      "USERNAME": "myuser",
      "PASSWORD": "super-secret-password",
      "DB": "mydb"
    }
  },
  "side_containers": {
    "mongo": {
      "image": "mongo",
      "environment": {
        "MONGO_INITDB_ROOT_USERNAME": "myuser",
        "MONGO_INITDB_ROOT_PASSWORD": "super-secret-password"
      },
      "volumes": [
        "/var/opt/loko/mongo/db:/data/db"
      ],
      "ports": {
        "27017": null
      }
    },
    "mongo_gui": {
      "image": "ugleiton/mongo-gui",
      "ports": {
        "4321": null
      },
      "environment": {
        "MONGO_URL": "mongodb://myuser:super-secret-password@mongo_extension_mongo:27017"
      },
      "expose": [
        4321
      ],
      "gui": {
        "name": "db manager",
        "path": "/",
        "gw": false
      }
    }
  }
}
```


