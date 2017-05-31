import os
import sys

# test if the persisnt is mounted
if not os.path.isdir('/persistent'):
    print('Persistent folder "/persistent" does not exist (it was probaly not mounted).')
    sys.exit()

# the shared folder /persistent/share is owned by admin, others can just read
if not os.path.isdir('/persistent/share'):
    os.system('mkdir /persistent/share')
os.system('chown -R admin:users /persistent/share')
os.system('chmod -R 666 /persistent/share')

# the admin user folder must contain a users folder
if not os.path.isdir('/home/admin/UsersFolder/'):
    os.system('mkdir /home/admin/UsersFolder/')

# the common folder /persitent/share is owned by admin, others can read and write
if not os.path.isdir('/persistent/common'):
    os.system('mkdir /persistent/common')
os.system('chown -R admin:users /persistent/common')

def create_user_folder(user, addShare=True, addCommonFolder=True):

    # create user folder if not exists and set right user to it
    if not os.path.isdir('/persistent/%s' % (user,)):
        os.system('mkdir /persistent/%s' % (user,))
    cmd = 'chown -R %s:users /persistent/%s' % (user, user)
    os.system(cmd)

    # the shared folder /persistent/share is owned by admin, others can just read
    if addShare and not os.path.isdir('/home/%s/SharedFolder' % (user,)):
        os.system('ln -s /persistent/share /home/%s/SharedFolder' % (user,))

    # the common folder /persistent/common is owned by admin, others can read and write
    if addCommonFolder and not os.path.isdir('/home/%s/CommonFolder' % (user,)):
        os.system('ln -s /persistent/common /home/%s/CommonFolder' % (user,))

    # add the user folder into the admin folder
    if not os.path.isdir('/home/admin/UsersFolder/%s' % (user,)):
        os.system('ln -s /persistent/%s /home/admin/UsersFolder/%s' % (user, user))

    
users = open('users','r').readlines()
    
for l in users:
    if len(l)>3:
        l2 = l.replace('\n','').split(':')
        user = l2[0]
        pwd  = l2[1]
        create_user_folder(user)
