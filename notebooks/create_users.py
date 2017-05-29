import os

users = open('users','r').readlines()

for l in users:
    if len(l)>3:
        l2 = l.replace('\n','').split(':')
        user = l2[0]
        pwd  = l2[1]
        os.system('useradd %s -s /bin/bash -m -g users' % (user,))

os.system('chpasswd < users')
