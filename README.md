# JupyterHub Docker Configuration

* Author: Jan Krause
* Initial version: 2017-05-29
* License: [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)

**This Docker configuration generates a fully configured JupterHub server, with simplified user management, optional persistent folders, and support for Python3, R, Octave, Javascript and BASH Jupyter Notebooks.**

![Logos](logos.png)

Configuration: 

* **configurable users** (listed in a file)
* **secured by HTTPS** (options: auto-signed certificates, classic certifcates, or using letsencrpyt)
* **optional persistent folders**: personal and shared folders on the host
* Jupyter languages support:
  * **Python3** : matplotlib, numpy, networkx, pandas, seaborn, posgresql, hdf5, spqarql, scikit-learn, nltk, elasticsearch ipythonwidgets...
  * **R-Project** : ggplot2, knitr, rmarkdown
  * **Octave**
  * **BASH**

Additional tools (accessible from the Jupyter terminal and BASH notebooks):

* shells: sh, bash
* editors: vi, vim, nano, emacs
* network: ssh, wget, rsync, curl, nmap
* file management: midnight commander
* images: ImageMagick
* computational workflow: SnakeMake
* text: pandoc, (pdf/xe)latex

# Getting started

## Install docker

This depend on you the host system (see [full documentation](https://docs.docker.com/engine/installation/)). On Ubuntu systems just:

    sudo apt update
    sudo apt install docker.io

## Configuration

### Users
Edit the file ./notebooks/users . Add a user per line. Syntax, a user per line usging the format: user:password . The user `admin` is mandatory. Default for admin password is "asdf1234".

Container system root password is changed via Dockerfile, the default is "asdf1234".

### HTTPS configuration

Use self-signed ssl certificates (some are provided by default, if you do not want to create yours skip this section). Generate auto-signed SSL certificate:

    cd notebooks
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 10000
    openssl rsa -in key.pem -out key-no-passwd.pem 
    cd ..

For other options, see below in the section `Alternative SSL configurations`.

## Build Docker image

Goto directory containing this docker file and execute:

    sudo docker build -t jankrause/jupyterhub .

## Run Docker image

There are several ways to run the container:

Run jupyterhub without persisting folder:

    sudo docker run -it -p 8001:8000 jankrause/jupyterhub bash runjupyterhub.bash

Run jupyterhub in the container using persistent folders (you have to specify the path on host by replacing /path/to/host/share in the line below):

    sudo docker run -it -p 8001:8000 -v `pwd`/persistent/:/persistent jankrause/jupyterhub bash runjupyterhub_with_share.bash

For production, the container can be executed via the deamon (so it is notably restarted automatically at host system reboot):

    sudo docker run -dit --restart always -p 443:8000 -v `pwd`/persistent/:/persistent jankrause/jupyterhub bash runjupyterhub_with_share.bash

An alternative, the container may be executed with an interactive BASH shell. This allows you to make temporary modifications to the system before running jupyterhub:

    sudo docker run -it -p 8001:8000 -v `pwd`/persistent/:/persistent jankrause/jupyterhub bash runjupyterhub
    # do some adjustments
    # - create users
    # - install applications
    # - ...
    bash add_shared_folders.py
    jupyterhub -f jupyterhub_config.py 

Finally in any case navigate using with the host's browser to:

    https://127.0.0.1:8001
    
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


## Mounting a volume (persistent folders)

When re-building or even re-executing the Docker container, e.g. at a system reboot or to add some new user or python package, all user data is destroyed. This can be useful for temporary systems, e.g. for one day trainings. 

For persisting configurations, you may want to mount an external filesystem, e.g. a folder of the host system:

    sudo docker run -it -p 8001:8000 -v `pwd`/persistent/:/persistent jankrause/jupyterhub
    sudo docker run -it -p 8001:8000 -v `pwd`/persistent/:/persistent jankrause/jupyterhub runjupyterhub_with_share.bash
    
In the "share" folder of the host create one folder for each user (using user name) and an additional folder named "share". Then uncomment the following line in the docker file (by removing the leading hash "#"):
    
    RUN python3 add_shared_folders.py


## Alternative SSL configurations


### Existing certificate
Alternatively you may use a proper pair of key/certificate. In this case name them cert.pem and key-no-passwd.pem. Pay attention that the key must not be protected by a pass phrase (the second openssl command just above is a way to remove the pass phrase of an existing key).

The key and certificates to use are defined in the notebooks/jupyterhub_config_autosigned.py like so:

    c.JupyterHub.ssl_cert = '/opt/notebooks/cert.pem'
    c.JupyterHub.ssl_key = '/opt/notebooks/key-no-passwd.pem'

### Use Let's Encrypt (via Certbot)

Retirements: ports 80 and 443 must be available for this to work, in other words you need to forward the to the host with the options -p 80:80 -p 443:443 when running the container.

Edit the file notebooks/domain . Add your domain name on the first line. In the Dockerfile, uncomment the section under `# Inatall Certbot`.

With this option, when running the container, you will have to execute:

    sudo docker run -it -p 8001:8000 -p 80:80 -p 443:443 jupyterhub -f /opt/notebooks/jupyterhub_config_certbot.py

### Deactivate SSL

If you wish to deactivate SSL, which is not recommended, just comment out the following lines in notebooks/jupyterhub.py like so: 

    #c.JupyterHub.ssl_cert = '/opt/notebooks/cert.pem'
    #c.JupyterHub.ssl_key = '/opt/notebooks/key-no-passwd.pem'

Then, you will have to start jupyterhub with the folloing command:

    sudo docker run -it -p 8001:8000 jupyterhub --no-ssl

## Configuration with other Docker services

### ElasticSearch

Elasticsearch is not included in this docker Image, but it can be executed in another container on the. To download the official conatiner:

    sudo docker pull elasticsearch
    
    
Then run elasticsearch and link the jupyterhub container in the same docker network

    sudo docker network create jupyterhubnet
    sudo docker run -d -p 9200:9200 -p 9300:9300 --name elastic --net jupyterhubnet elasticsearch
    sudo docker run -d -p 8005:8000 -v `pwd`/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub runjupyterhub_with_share.bash
    
With that configuration, the ElasticSearch service will be reachable form JupyterHub using the 'elastic' host name on pourt 9200 (default). From a Python notebook, it can be accessed the following way :

    from elasticsearch import Elasticsearch
    es = Elasticsearch('http://elastic:9200')


Elasticsearch data can also be persisted on host: 

    sudo docker network create jupyterhubnet
    sudo docker run -d -p 9200:9200 -p 9300:9300 -v `pwd`/elasticdata/:/usr/share/elasticsearch/data --name elastic --net jupyterhubnet elasticsearch
    sudo docker run -d -p 8005:8000 -v `pwd`/persistent/:/persistent --net jupyterhubnet jankrause/jupyterhub runjupyterhub_with_share.bash
