#!/bin/sh

docker pull elasticsearch
docker build -t jankrause/jupyterhub .
docker network create jupyterhubnet
docker run -d --restart always -p 9200:9200 -p 9300:9300 --name elastic --net jupyterhubnet elasticsearch
docker run -d --restart always -p 443:8000 -v /opt/JupyterHubDocker/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub bash runjupyterhub_with_share.bash

