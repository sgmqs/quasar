import os
import subprocess

import quasar.config as sql_config

def get_filelist(dirname):
    filelist = os.listdir(dirname)
    return filelist

filelist = get_filelist('./data/sql/migrations/')
print(sql_config.user)

for file in filelist:
    with open('./data/sql/migrations/%s' % file, 'r') as f:
        command = ['mysql', '-u%s' % sql_config.user,
                   '-p%s' % sql_config.pw,
                   '--host=%s' % sql_config.host,
                   '--port=%s' % sql_config.port]
        proc = subprocess.Popen(command, stdin = f)
        stdout, stderr = proc.communicate()
