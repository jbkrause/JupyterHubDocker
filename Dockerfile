### start from base ###

FROM ubuntu:16.04
MAINTAINER Jan Krause <jk.work@protonmail.ch>

### copy configuration to container ###
ADD notebooks /opt/notebooks
WORKDIR /opt/notebooks

### use better sources (good mirror selected by geoIP) ###
# Remark : this is specific for ubuntu 16.04 xenial
# if you change ubuntu version adapt souces.list or coment this line out.
RUN cp sources.list /etc/apt/sources.list

### update packgages ###
RUN apt-get -yqq update

### install usefull tools (for jupyter terminal) ###
RUN apt-get -yqq install apt-utils
RUN apt-get -yqq install emacs
RUN apt-get -yqq install vim
RUN apt-get -yqq install mc
RUN apt-get -yqq install imagemagick
RUN apt-get -yqq install texlive
RUN apt-get -yqq install texlive-latex-extra
RUN apt-get -yqq install pandoc 
RUN apt-get -yqq install rsync
RUN apt-get -yqq install curl

### installing python packages and building pandas ###
RUN apt-get -yqq install python3-pip
RUN apt-get -yqq install python3-pil
RUN apt-get -yqq install python3-requests
RUN apt-get -yqq install python3-dev
RUN apt-get -yqq install npm
RUN apt-get -yqq install nodejs-legacy
RUN npm install -g configurable-http-proxy

# fetch python specific libraries
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

### installing octave ###
RUN apt-get -yqq install octave
RUN python3 -m octave_kernel.install

### installing R-project ###
RUN bash install_r.bash

### install jupyter kernels and widgets ###
RUN python3 -m bash_kernel.install

### activate ipython widgets ###
RUN jupyter nbextension enable --py --sys-prefix widgetsnbextension

### users creation (based on the file notebooks/users) ###
RUN python3 create_users.py

# Install Certbot (ssl certificat generation based on the file notebooks/domain)
#RUN apt-get -yqq install software-properties-common
#RUN add-apt-repository -y ppa:certbot/certbot
#RUN apt-get -yqq update
#RUN apt-get -yqq install certbot
#RUN python3 ssl_certbot.py

# expose port
EXPOSE 8000

# start app
#CMD ["jupyterhub", "-f", "jupyterhub_config.py"]
#CMD ["bash", "runjupyterhub_with_share.bash"]
CMD ["bash"]


