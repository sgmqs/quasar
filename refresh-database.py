import os
import subprocess

from quasar.config import config


def get_filelist(dirname):
    filelist = os.listdir(dirname)
    return filelist

filelist = get_filelist('./data/sql/migrations/')

for file in filelist:
    with open('./data/sql/migrations/%s' % file, 'r') as f:
        command = ['mysql', '-u%s' % config.user,
                   '-p%s' % config.pw,
                   '--host=%s' % config.host,
                   '--port=%s' % config.port]
        proc = subprocess.Popen(command, stdin=f)
        stdout, stderr = proc.communicate()
