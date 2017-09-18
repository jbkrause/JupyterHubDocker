# JupyterHub Docker

* Author : Jan Krause
* Initial version : 2017-05-29
* Version 1.0.0 : 2017-09-18
* License : [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

** This Docker configuration generates a fully configured JupterHub server**, with::
* simplified user management, 
* persistent folders: personal folders (private), shared folder (anybody can edit), read-only folder (only admin can modiy),
* Jupyter secured by HTTPS
* HTTP service of the "Shared" folder, for publication (e.g. diffusion via http://nbviewer.jupyter.org)
* User can access their folders remotely and securely via SFTP
* ready to interoperate with Postgresql and ElasticSearch containers

![Logos](logos.png)

* Defaull packages:
  * **Python3** : matplotlib, numpy, networkx, pandas, seaborn, sqlalchemy (notably posgresql), hdf5, spqarql, scikit-learn, nltk, elasticsearch, ipythonwidgets...
  * **R-Project** : ggplot2, knitr, rmarkdown
  * **Octave**
  * **BASH**
  * **Javascript**

Additional tools (accessible from the Jupyter terminal and BASH notebooks):

* shells: sh, bash
* editors: vi, vim, nano, emacs
* network: ssh (client and server), wget, rsync, curl, nmap, pgsql (postgresql)
* file management: midnight commander
* images: ImageMagick
* computational workflow: SnakeMake
* text: pandoc, (pdf/xe)latex

# Getting started

## Quick start using pre-build image

Download:

    docker pull jankrause/jupyterhub

Run (the container will restart automatically when host reboots):

    sudo docker run -d --restart always -p 80:80 -p 443:8000 -p 222:22 -v /opt/JupyterHubDocker/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub bash runjupyterhub.bash

Access to JupyterHub from a web browser:

    * https://127.0.0.1
    * Add a security exception, this is necessary since the SSL certificate was autosigned (see below how to install proper certificates)
    * Administration: user 'admin' ; password 'asdf1234'
    * Users: user1, user2 ... user15 ; passwords 'asdf1234'

Public access to the files in the 'Sahre' folder:

    * http://127.0.0./example.ipynb

Administration via SSH from host:

    * ssh -p 222 root@127.0.0.1
    * password: 'asdf1234'

## Build form source

### Users

Edit the file ./notebooks/users . Add a user per line. Syntax, a user per line usging the format: user:password . The user `admin` is mandatory. Default for admin password is "asdf1234".

Container system root password is changed via Dockerfile, the default is "asdf1234".

Important note: you should change the root password, that is defined in the Dockerfile, defaul is 'asdf1234'.

## Build Docker image

Goto directory containing this docker file and execute:

    sudo docker build -t jankrause/jupyterhub .

## Run Docker image

There are several ways to run the container:

Run jupyterhub:

    sudo docker run -d --restart always -p 80:80 -p 443:8000 -p 222:22 -v `pwd`/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub bash runjupyterhub.bash

Finally in any case navigate using with the host's browser to:

    https://127.0.0.1
    
* Note 1: if using an auto-signed certificate, you have to override the security warning in your browser.
* Note 2: default user is "admin" with password "asdf1234" (if you have not, you should change that; users can be defined in the notebooks/users file, one per line, following the syntax user:password

# Additional documentation

## User management
* users are created by the script create_users.py
  * this script creates the users listed in the file "notebooks/users"
  * in this file add one user per line using the syntax user:password
* in notebooks/jupyter_config.py : 
  * admins are defined at the line:
     c.Authenticator.admin_users = {'admin'}
  * a whitelist can be added like thus (and this is recommended):
     c.Authenticator.whitelist = {'admin','jan'}


## Additional packages

### Python
The packages listed in notebooks/requirements.txt are installed using pip3. If you wish to add/remove/modify installed packages by editing in this file. Available packages and their versions may be browsed on http://pypi.org .

### R
Installed CRAN packages are listed in the file notebooks/install_r.bash . You may add/remove/modify installed packages by editing the line beginning with `echo "install.packages`. Available packages are listed on the following website https://cran.r-project.org/web/packages/available_packages_by_name.html .


## SSL configuration

## Use a custom made self-signes SSL certificate

A selfsigned SSL certificates are provided by default. But you can generate your own self-signed SSL certificate to:

    cd notebooks
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 10000
    openssl rsa -in key.pem -out key-no-passwd.pem 
    cd ..

# Use valid SSL certificate
Alternatively you may use a proper pair of key/certificate. In this case name them cert.pem and key-no-passwd.pem. Pay attention that the key must not be protected by a pass phrase. You may buy such certificates from specialized companies, e.g.Gandi.net .

The key and certificates to use are defined in the notebooks/jupyterhub_config_autosigned.py like so:

    c.JupyterHub.ssl_cert = '/opt/notebooks/cert.pem'
    c.JupyterHub.ssl_key = '/opt/notebooks/key-no-passwd.pem'


### Deactivate SSL

If you wish to deactivate SSL, which is not recommended, just comment out the following lines in notebooks/jupyterhub.py like so: 

    #c.JupyterHub.ssl_cert = '/opt/notebooks/cert.pem'
    #c.JupyterHub.ssl_key = '/opt/notebooks/key-no-passwd.pem'

Then, you will have to start jupyterhub with the folloing command:

    sudo docker run -it -p 8001:8000 jupyterhub --no-ssl

## Configure compatible Docker services

### ElasticSearch

Elasticsearch is not included in this docker image, but it can be executed within in another Docker container on the host. To download the official conatiner:

    sudo docker pull elasticsearch
    
Then run elasticsearch and link the jupyterhub container in the same docker network

    sudo docker network create jupyterhubnet
    sudo docker run -d --restart always -p 9200:9200 -p 9300:9300 --name elastic --net jupyterhubnet elasticsearch
    sudo docker run -d --restart always -p 80:80 -p 443:8000 -p 222:22 -v /opt/JupyterHubDocker/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub bash runjupyterhub.bash
    
With that configuration, the ElasticSearch service will be reachable form JupyterHub using the 'elastic' host name on port 9200 (default). From a Python notebook, it can be accessed the following way :

    from elasticsearch import Elasticsearch
    es = Elasticsearch('http://elastic:9200')


ElasticSearch data can also be persisted on the host (or any host mount point): 

    sudo docker network create jupyterhubnet
    sudo docker run -d --restart always -p 9200:9200 -p 9300:9300 -v `pwd`/elasticdata/:/usr/share/elasticsearch/data --name elastic --net jupyterhubnet elasticsearch
    sudo docker run -d --restart always -p 80:80 -p 443:8000 -p 222:22 -v /opt/JupyterHubDocker/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub bash runjupyterhub.bash
    
## Postgresql

The approach is similar as for ElasticSearch just above:

    sudo docker pull postgres
    sudo docker network create jupyterhubnet
    sudo docker run -d --restart always --name postgres -e POSTGRES_PASSWORD=asdf1234 -p 5432:5432 --net jupyterhubnet  postgres
    sudo docker run -d --restart always -p 80:80 -p 443:8000 -p 222:22 -v /opt/JupyterHubDocker/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub bash runjupyterhub.bash




