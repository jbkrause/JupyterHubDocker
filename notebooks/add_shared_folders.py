import os

users = open('users','r').readlines()

# the common folder /share/share is owned by admin, others can just read
os.system('chown -R admin:users /share/share')

for l in users:
    if len(l)>3:
        l2 = l.replace('\n','').split(':')
        user = l2[0]
        pwd  = l2[1]
        cmd = 'chown -R %s:users /share/%s' % (user, user)
        print(cmd)
        os.system(cmd)
        os.system('ln -s /share/%s /home/%s/myFolder' % (user, user))
        os.system('ln -s /share/%s /home/admin/users/%s' % (user, user))
        os.system('ln -s /share/share /home/%s/commonFolder' % (user,))

#os.system('chmod -R 666 /share/*')


