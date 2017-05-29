apt-get -yqq install r-base
apt-get -yqq install curl
apt-get -yqq install libcurl4-gnutls-dev
echo "install.packages(c('repr', 'IRdisplay', 'crayon', 'pbdZMQ', 'devtools', 'ggplot2', 'knitr', 'rmarkdown'), repos = 'http://cran.us.r-project.org', dependencies = TRUE)" > Jupyter.R
echo "devtools::install_github('IRkernel/IRkernel')" >> Jupyter.R
echo "IRkernel::installspec(user = FALSE)" >> Jupyter.R
Rscript Jupyter.R

