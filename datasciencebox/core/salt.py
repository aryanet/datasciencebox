from __future__ import absolute_import, unicode_literals

import subprocess

from fabric.api import settings, run, sudo, hide


master_roles = ['miniconda', 'zookeeper', 'mesos.master', 'namenode', 'ipython.notebook', 'spark']
minion_roles = ['miniconda', 'mesos.slave', 'datanode']


def salt_ssh(project, target, module, args=None, kwargs=None):
    args = args or []
    kwargs = kwargs or []
    target = target or '"*"'

    cmd = ['salt-ssh', target, module]

    for arg in args:
        cmd.append(arg)
    for key in kwargs:
        cmd.append('{0}={1}'.format(key, kwargs[key]))

    cmd.append('--state-output=mixed')
    cmd.append('--roster-file=%s' % project.roster_path)
    cmd.append('--config-dir=%s' % project.salt_ssh_config_dir)
    cmd.append('--ignore-host-keys')
    cmd = ' '.join(cmd)
    print(cmd)

    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if proc.returncode != 0 or err:
        raise Exception(err)
    print out
    return proc.returncode, out, err


def salt_master(project, target, module, args=None, kwargs=None):
    args = args or []
    kwargs = kwargs or []
    target = target or '"*"'

    ip = project.cluster.master.ip
    username = project.settings['USERNAME']
    host_string = username + '@' + ip
    key_filename = project.settings['KEYPAIR']
    with hide('running', 'stdout', 'stderr'):
        with settings(host_string=host_string, key_filename=key_filename):
            cmd = ['sudo', 'salt', target, module]

            for arg in args:
                cmd.append(arg)
            for key in kwargs:
                cmd.append('{0}={1}'.format(key, kwargs[key]))

            cmd.append('--timeout=300')
            cmd.append('--state-output=mixed')
            cmd = ' '.join(cmd)
            print(cmd)

            out = sudo(cmd)
            print(out)
