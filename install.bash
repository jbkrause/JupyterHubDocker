#sudo docker pull elasticsearch
#sudo docker pull postgres

sudo docker build -t jankrause/jupyterhub .

sudo docker network create jupyterhubnet

#sudo docker run -d --restart always --name postgres -e POSTGRES_PASSWORD=asdf1234 -p 5432:5432 --net jupyterhubnet  postgres
#sudo docker run -d --restart always -p 9200:9200 -p 9300:9300 --name elastic --net jupyterhubnet elasticsearch

sudo docker run -d --restart always -p 80:80 -p 443:8000 -p 222:22 -v /opt/JupyterHubDocker/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub bash runjupyterhub.bash

