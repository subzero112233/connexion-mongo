# Connexion Example REST API with MongoDB

This example application implements a basic REST API for storing and retrieving NBA player's data, using: Python, OpenAPI, Connexion and MongoDB.


This example covers:
* Specification mapping, serialization of payloads and schema validation with OpenAPI and Connexion
* Storing the CRUD service data in MongoDB
* Running it all together in docker with docker-compose


# Installation
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose up --build
```

# Local development
```sh
pip3 install -r app/requirements.txt
docker-compose up mongo
python3 app.py
```
