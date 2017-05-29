import os

domains = open('domain','r').readlines()
domain = domains[0].replace('\n','')
email = domains[1].replace('\n','')
workdir = os.getcwd()

os.system('certbot certonly -n --agree-tos --standalone -m %s -d %s' % (email, domain))

