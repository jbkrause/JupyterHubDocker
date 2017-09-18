#!/bin/bash

cwd=$(pwd)
cd /home

for user in user*
do
    echo "$user"
    cp -R "$cwd/$1" "/home/$user/Documents"
    chown -R $user:users "/home/$user/Documents/$1"
done
