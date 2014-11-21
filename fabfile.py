# Note: fabric must be run with python2.6
import json
import datetime
from socket import error as SocketError
import time
from fabric.api import *
from fabric.contrib.files import append, put, sed, exists
from fabric.colors import *
import boto
import boto.ec2
import paramiko


def _stamp(title='', color=blue, bold=False):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if callable(color):
        print(color('%s %s' % (now, title), bold=bold))
    else:
        print('%s %s' % (now, title))

PROJECT = "BankValDj"
SECRETFILE = './%s/settings/secret/server_config_secret.json' % PROJECT
with open(SECRETFILE) as f:
    all_servers = json.loads(f.read())
if not env.hosts or not env.hosts[0] in all_servers:
    _stamp('Instance name not specified or not in server config file', color=red, bold=True)
    _stamp('Fabric should be called using "fab -H <instance name>" e.g. fab deploy -H production', color=red)
    _stamp('where <instance> is defined in the <project/settings/secret/server_config_secret file', color=red)
    exit(1)
server = all_servers[env.hosts[0]]
server['instance_name'] = env.hosts[0]  # use the host parameter as the instance name
env.hosts = server['ip_address']  # fabric always accesses instance by ip address
HOST = server['dns_hostname'].encode() if server['dns_hostname'].encode() != '' else server['ip_address'].encode()
env.key_filename = server['key_file_name']
env.user = server['username']
env.disable_known_hosts = True  # avoid exception where host changes its host key
LOGDIR = '/home/%s/log/' % env.user
SITE_ROOT = '/home/{user}/{project}/'.format(user=env.user, project=PROJECT)
SITE_PROJECT_ROOT = SITE_ROOT + PROJECT + '/'
LOCAL_ROOT = '~/Documents/Projects/{project}/'.format(project=PROJECT)
LOCAL_PROJECT_ROOT = LOCAL_ROOT + PROJECT + '/'


##################### fabric callables below this line #####################
def commit(note="fixes"):
    local('git add -A')
    local('git commit -a -m %s' % note)
    local('git push')


def deploy():
    _stamp('Beginning deployment to %s' % server['instance_name'], color=blue, bold=True)
    local('git push %s' % server['instance_name'])
    put('{0}settings/secret/*'.format(LOCAL_PROJECT_ROOT), '{0}settings/secret/'.format(SITE_PROJECT_ROOT), mode=0o0600)
    append('{0}settings/secret/production.py'.format(SITE_PROJECT_ROOT),
           'ALLOWED_HOSTS = ["{0}","www.{0}","{1}"]'.format(HOST, server['ip_address']))
    sed('{0}celeryapp.py'.format(SITE_PROJECT_ROOT), 'settings.local', 'settings.production')
    run('touch /tmp/uwsgi.touch')
    _stamp('Deployment to %s complete' % server['instance_name'], color=green, bold=True)


def deployfile(filename):
    put('{0}{1}'.format(LOCAL_ROOT, filename), '{0}{1}'.format(SITE_ROOT, filename))


################  build an amazon ec2 instance "fab create_server setup_server -H <instance name>" ##############
def create_server():
    _stamp('Creating instance %s' % server['instance_name'], color=blue, bold=True)
    # get connection to server services
    conn = boto.ec2.connect_to_region(server['region'], aws_access_key_id=server['access_key_id'],
                                      aws_secret_access_key=server['secret_access_key'])
    dev_xvda = boto.ec2.blockdevicemapping.EBSBlockDeviceType(connection=conn, volume_type='gp2')  # general purpose SSD
    bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
    bdm['/dev/xvda'] = dev_xvda

    # create reservation and start instance
    image = conn.get_all_images(server['ami_list'])
    reservation = image[0].run(1, 1, key_name=server['key_pair_name'], security_groups=server['security_group'],
                               instance_type=server['instance_type'], block_device_map=bdm)
    instance = reservation.instances[0]
    conn.create_tags([instance.id], {"Name": server['instance_name']})
    _stamp('Waiting for instance to be created before checking status', color=cyan)
    time.sleep(10)
    while instance.state == u'pending':
        instance.update()
        _stamp("Instance creation %s - waiting 3 more seconds" % instance.state, color=cyan)
        time.sleep(3)

    # allocate an elastic ip address and set env.hosts for next config steps
    addr = conn.allocate_address("vpc")
    conn.associate_address(instance_id=instance.id, allocation_id=addr.allocation_id)
    instance.update()
    env.hosts = [instance.ip_address, ]
    _stamp('Instance "%s" created successfully with elastic ip %s'
           % (server['instance_name'], instance.ip_address), color=green)
    server['ip_address'] = instance.ip_address
    all_servers[server['instance_name']] = server
    with open(SECRETFILE, 'w') as jsonFile:      # update json file ip_address for this server to cater for reruns
        jsonFile.write(json.dumps(all_servers, indent=2))

    _stamp("About to test SSH Connection to %s as user %s" % (instance.ip_address, env.user), color=cyan)
    _stamp("Waiting for instance to start for 40 seconds before attempting to connect up to 15 times", color=cyan)
    time.sleep(35)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for attempt in range(1, 15):
        try:
            time.sleep(5)
            ssh.connect(instance.ip_address, username=env.user, key_filename=server['key_file_name'], timeout=5)
        except SocketError:
            _stamp("Waiting for instance to start - attempt %s" % attempt, color=cyan)
        else:
            stdin, stdout, stderr = ssh.exec_command('echo "%s SSH%s"' % (server['instance_name'], instance.ip_address))
            _stamp(stdout.readlines()[0]+'\n', color=green, bold=True)
            ssh.close()
            break
    else:
        raise RuntimeError(red('maximum number of unsuccessful attempts reached', bold=True))


def remote_basic_setup():
    _stamp('Setting up remote basics - directories, timezone etc', color=blue, bold=True)
    sudo('rm -rf /home/%s/*' % env.user)  # zap anything from previous run even if owned by root
    run('mkdir -p {0}'.format(LOGDIR))
    run('mkdir -p ~/{0}'.format(PROJECT))
    run('mkdir -p {0}log'.format(SITE_ROOT))
    sudo('mv -f /etc/localtime /etc/localtime.old')
    sudo('ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime')
    _stamp('Remote basics successfully setup\n', color=green, bold=True)


def local_ssh_config():
    _stamp('Creating local SSH config', color=blue, bold=True)
    contents = local('cat ~/.ssh/config', capture=True)
    if 'Host ' + server['instance_name'] in contents and 'Hostname ' + server['ip_address'] in contents:
        _stamp('Skipping ~/.ssh/config setup as host already configured')
    else:
        local('echo "\nHost %s\nHostname %s \nUser %s \nIdentityFile %s \n" >> ~/.ssh/config'
              % (server['instance_name'], server['ip_address'], env.user, env.key_filename))
    local('ssh-keyscan %s >> ~/.ssh/known_hosts' % server['ip_address'])
    _stamp('Note: bad hostkey message above can be ignored if two hostkeys are displayed', color=None)
    _stamp('Local SSH configured successfully\n', color=green, bold=True)


def install_python(force=False):
    _stamp('Installing Python (takes a few mins)', color=blue, bold=True)
    if exists('/usr/local/bin/python3') and not force:
        _stamp('Python already installed (use "force=True" to uninstall/re-install)\n',  color=yellow, bold=True)
        return
    run('touch {0}python_install.log'.format(LOGDIR))  # create log file under normal user
    sudo('yum -y update > {0}yumupdate.log'.format(LOGDIR))
    sudo('yum -y install gcc make openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel >>'
         ' {0}python_install.log'.format(LOGDIR))
    run('wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tar.xz >> {0}python_install.log'.format(LOGDIR))
    run('tar -Jxf Python-3.4.1.tar.xz')
    with cd('Python-3.4.1'):
        run('./configure --prefix=/usr/local/python --enable-shared >> {0}python_install.log'.format(LOGDIR))
        run('make >> python_install.log')
        sudo('make install >> {0}python_install.log'.format(LOGDIR))
    append('/etc/ld.so.conf', '/usr/local/python/lib', use_sudo=True)
    sudo('ldconfig')
    sudo('ln -sf /usr/local/python/bin/python3 /usr/local/bin/python3')
    sudo('ln -sf /usr/local/python/bin/pip3 /usr/local/bin/pip')
    sudo('ln -sf /usr/local/python/bin/virtualenv /usr/local/bin/virtualenv')
    sudo('ln -sf /usr/local/bin/python3 /usr/local/bin/python')
    _stamp('Python installed successfully\n', color=green, bold=True)


# TODO replace with virtualenvwrapper
def install_virtualenv():
    _stamp('Installing virtualenv', color=blue, bold=True)
    sudo('/usr/local/bin/pip install virtualenv > {0}virtualenv_install.log'.format(LOGDIR))
    run('virtualenv -p /usr/local/bin/python3 {0}'.format(PROJECT))
    _stamp('Virtualenv installed successfully\n', color=green, bold=True)


def install_mysql(force=False):
    _stamp('Installing mysql', color=blue, bold=True)
    with hide('output'):
        if 'mysql' in sudo('yum list installed'):
            if force:
                sudo('service mysqld stop')
                sudo('yum -y groupremove "MySQL Database" > {0}mysql_remove.log'.format(LOGDIR))
                sudo('rm -rf /var/lib/mysql')
            else:
                _stamp('MySQL already installed (use "force=True" to uninstall/re-install)\n', color=yellow, bold=True)
                return
    sudo('yum -y groupinstall "MySQL Database" > {0}mysql_install.log'.format(LOGDIR))
    sudo('chkconfig mysqld on')
    sudo('service mysqld start')
    run('mysql -u root -e "create database {0}";'.format(PROJECT.upper()))
    with settings(prompts={
        'Enter current password for root (enter for none): ': '\n',
        'Set root password? [Y/n] ': '\n',
        'New password: ': server['mysql_password'],
        'Re-enter new password: ': server['mysql_password'],
        'Remove anonymous users? [Y/n] ': '\n',
        'Disallow root login remotely? [Y/n] ': '\n',
        'Remove test database and access to it? [Y/n] ': '\n',
        'Reload privilege tables now? [Y/n] ': '\n'
    }):
        run('mysql_secure_installation')
    _stamp('MySQL installed successfully\n', color=green, bold=True)


def install_git_and_code(force=False):
    _stamp('Installing git and project code', color=blue, bold=True)
    with hide('output'):
        if 'git.' in sudo('yum list installed'):
            if force:
                sudo('yum -y remove git > {0}git_remove.log'.format(LOGDIR))
                sudo('yum -y install git > {0}git_install.log'.format(LOGDIR))
            else:
                _stamp('git already installed,(use "force=True" to uninstall/re-install)\n', color=yellow, bold=True)
        else:
            sudo('yum -y install git > {0}git_install.log'.format(LOGDIR))
    sudo('rm -rf /home/%s/.%s.git' % (env.user, PROJECT))
    run('mkdir ~/.%s.git' % PROJECT)
    with settings(warn_only=True):
        local('git remote remove %s' % server['instance_name'])
        local('git remote add {0} ssh://{0}/home/{1}/.{2}.git'.format(server['instance_name'], env.user, PROJECT))
    with cd('~/.%s.git' % PROJECT):
        run('git init --bare')
        append('hooks/post-receive', '#!/bin/sh \nGIT_WORK_TREE=~/%s git checkout -f \n' % PROJECT)
        run('chmod +x hooks/post-receive')
    _stamp('git installed successfully\n', color=green, bold=True)

    _stamp('Now installing Django Project code', color=blue, bold=True)
    local('git push {0} +master:refs/heads/master'.format(server['instance_name']))
    run('mkdir -p {0}settings/secret'.format(SITE_PROJECT_ROOT))
    put('{0}settings/secret/*'.format(LOCAL_PROJECT_ROOT), '{0}settings/secret/'.format(SITE_PROJECT_ROOT), mode=0o0600)
    _stamp('Modifying config files for deployment environment', color=cyan)
    append('{0}settings/production.py'.format(SITE_PROJECT_ROOT),
           'ALLOWED_HOSTS = ["{0}","www.{0}","{1}"]'.format(HOST, server['ip_address']))
    sed('{0}celeryapp.py'.format(SITE_PROJECT_ROOT), 'settings.local', 'settings.production')
    _stamp('Django project code installed successfully\n', color=green, bold=True)


def remote_profile():
    _stamp('Updating remote bash_profile', color=blue, bold=True)
    text = "\n#### fabric-added django config below this line #### \
        \nsource ~/{0}/bin/activate \
        \nalias m='./manage.py' \
        \nexport DJANGO_SETTINGS_MODULE={0}.settings.production \
        \nexport PYTHONPATH=~/{0}/lib/python3.4/site-packages:~/{0}\n".format(PROJECT)
    append('~/.bash_profile', text)
    _stamp('Remote bash_profile updated successfully\n', color=green, bold=True)


def install_requirements():
    _stamp('Installing requirements with pip', color=blue, bold=True)
    run('which python')  # display python version/env for upcoming install
    run('pip install -r {0}requirements/production.txt > {1}requirements_install.log'.format(SITE_ROOT, LOGDIR))
    run('pip freeze')  # display installed packages
    with cd(PROJECT):
        run('./manage.py collectstatic --noinput >> {0}requirements_install.log'.format(LOGDIR))
        run('./manage.py makemigrations')
        run('./manage.py migrate')
        with settings(prompts={
            "Username (leave blank to use '{0}'): ".format(env.user): server['django_superuser'],
            'Email address: ': '\n',
            'Password: ': server['django_superuser_password'],
            'Password (again): ': server['django_superuser_password'],
        }):
            run('./manage.py createsuperuser')
    _stamp('Python requirements installed successfully\n', color=green, bold=True)


def install_nginx(force=False):
    _stamp('Installing nginx web server at address %s, port=80' % HOST, color=blue, bold=True)
    with hide('output'):
        if 'nginx' in sudo('yum list installed'):
            if force:
                sudo('service nginx stop')
                sudo('rm /etc/nginx/conf.d/nginx.conf')
                sudo('yum -y remove nginx > {0}nginx_remove.log'.format(LOGDIR))
                sudo('yum -y install nginx > {0}nginx_install.log'.format(LOGDIR))
            else:
                _stamp('nginx already installed(use "force=True" to uninstall/re-install)\n', color=yellow, bold=True)
        else:
            sudo('yum -y install nginx > %s/nginx_install.log' % LOGDIR)
    sed('{0}settings/nginx.conf'.format(SITE_PROJECT_ROOT), '<hostname>', HOST)
    sed('{0}settings/nginx.conf'.format(SITE_PROJECT_ROOT), '<ipaddress>', server['ip_address'])
    sed('{0}settings/nginx.conf'.format(SITE_PROJECT_ROOT), '<username>', env.user)
    sed('{0}settings/nginx.conf'.format(SITE_PROJECT_ROOT), '<project>', PROJECT)
    sudo('cp -f {0}settings/nginx.conf /etc/nginx/conf.d/'.format(SITE_PROJECT_ROOT))
    sudo('cp -f {0}settings/secret/ssl_secret* /etc/nginx/conf.d'.format(SITE_PROJECT_ROOT))
    sudo('chmod 600 /etc/nginx/conf.d/ssl_secret*')
    sudo('sudo usermod -a -G nginx {0}'.format(env.user))  # allow uwsgi to read files in nginx
    sudo('sudo usermod -a -G {0} nginx '.format(env.user))  # allow nginx to see static files
    sudo('chmod g+rx /home/{0}'.format(env.user))
    sudo('chmod 750 /var/log/nginx')
    sudo('chkconfig nginx on')
    sudo('service nginx restart')
    _stamp('Nginx installed successfully and started\n', color=green, bold=True)


def install_uwsgi():
    _stamp('Installing uWSGI server', color=blue, bold=True)
    sudo('mkdir -p /etc/uwsgi/vassals')
    sudo('mkdir -p -m 0750 /var/log/uwsgi')
    sudo('mkdir -p -m 0750 /var/run/uwsgi')
    sudo('chown -R {0}:nginx /var/log/uwsgi'.format(env.user))
    sudo('chown -R {0}:nginx /var/run/uwsgi'.format(env.user))
    sed('{0}settings/uwsgi.ini'.format(SITE_PROJECT_ROOT), '<username>', env.user)
    sed('{0}settings/uwsgi.ini'.format(SITE_PROJECT_ROOT), '<project>', PROJECT)
    sudo('cp -f {0}settings/uwsgi.ini /etc/uwsgi/vassals/'.format(SITE_PROJECT_ROOT))
    sudo("/usr/local/bin/pip install uwsgi > {0}uwsgi_install.log".format(LOGDIR))
    sudo("cp -f {0}settings/uwsgi.sh  /etc/init.d/uwsgi".format(SITE_PROJECT_ROOT))
    sudo('chown -R {0}:nginx /etc/init.d/uwsgi')
    sed('/etc/init.d/uwsgi', '<username>', env.user, use_sudo=True)
    sudo('chkconfig --add uwsgi; chkconfig uwsgi on')
    sudo('service uwsgi start'.format(env.user))
    _stamp('uWSGI installed successfully\n\n', color=green, bold=True)


def install_redis(force=False):
    _stamp('Installing redis server', color=blue, bold=True)
    if not exists('/usr/local/bin/redis-server') or force:
        sudo('yum -y install tcl > {0}redis_install.log'.format(LOGDIR))
        with hide('output'):
            sudo('wget http://download.redis.io/redis-stable.tar.gz >> {0}redis_install.log'.format(LOGDIR))
        sudo('tar xvzf redis-stable.tar.gz > {0}redis_install.log'.format(LOGDIR))
        with cd('redis-stable'):
            sudo('make >> {0}redis_install.log'.format(LOGDIR))
            # sudo('make test >> {0}redis_install.log'.format(LOGDIR))  # TAKES TOO LONG!!!
            with cd('src'):
                sudo('cp redis-benchmark redis-cli redis-server redis-check-aof redis-check-dump /usr/local/bin')
    with settings(prompts={
        'Please select the redis port for this instance: [6379] ': '\n',
        'Please select the redis config file name [/etc/redis/6379.conf] ': '\n',
        'Please select the redis log file name [/var/log/redis_6379.log] ': '\n',
        'Please select the data directory for this instance [/var/lib/redis/6379] ': '\n',
        'Please select the redis executable path [] ': '/usr/local/bin/redis-server',
        'Is this ok? Then press ENTER to go on or Ctrl-C to abort.': '\n'
    }):
        sudo('/home/{0}/redis-stable/utils/install_server.sh'.format(env.user, LOGDIR))
    sed('/etc/redis/6379.conf', 'appendonly no', 'appendonly yes', use_sudo=True)
    sudo('service redis_6379 restart')
    _stamp('redis installed successfully and started\n\n', color=green, bold=True)


def install_celery():
    _stamp('Installing celery', color=blue, bold=True)
    sudo('/usr/local/bin/pip install celery[redis] > %s/celery_install.log' % LOGDIR)
    sudo('cp {0}settings/celeryd.init /etc/init.d/celeryd; chmod 750 /etc/init.d/celeryd'.format(SITE_PROJECT_ROOT))
    sudo('cp {0}settings/celeryd.conf /etc/default/celeryd; chmod 640 /etc/default/celeryd'.format(SITE_PROJECT_ROOT))
    sed('/etc/default/celeryd', 'BIN="/usr/local/bin/celery"', 'BIN="{0}bin/celery"'.format(SITE_ROOT), use_sudo=True)
    sed('/etc/default/celeryd', 'APP="proj"', 'APP="%s:celery_app"' % PROJECT, use_sudo=True)
    sed('/etc/default/celeryd', 'CHDIR="/opt/Myproject/"', 'CHDIR="{0}"'
        .format(SITE_ROOT), use_sudo=True)
    sed('/etc/default/celeryd', 'USER="celery"', 'USER="%s:' % env.user, use_sudo=True)
    sudo('sudo chkconfig celeryd on')

    sudo('cp {0}settings/celerybeat.init /etc/init.d/celerybeat; chmod 750 /etc/init.d/celerybeat'
         .format(SITE_PROJECT_ROOT))
    sudo('cp /etc/default/celeryd /etc/default/celerybeat')
    sudo('sudo chkconfig celerybeat on')

    sed('{0}celeryapp.py'.format(SITE_PROJECT_ROOT), 'settings.local', 'settings.production')
    sudo('service celeryd restart')
    sudo('service celerybeat restart')
    _stamp('celery installed successfully and started\n\n', color=green, bold=True)


def cleanup_files():
    sudo('rm -rf ~/log ~/Python* ~/redis*')


# TODO consider deploying to a date stamped folder to enable easy rollback
def setup_server():
    """ Steps to build new server instance"""
    remote_basic_setup()
    local_ssh_config()
    install_python(force=False)
    install_virtualenv()
    install_mysql(force=True)
    install_git_and_code(force=False)
    remote_profile()
    install_requirements()
    install_nginx(force=True)
    install_uwsgi()
    install_redis(force=False)
    install_celery()
    _stamp('***SERVER SUCCESSFULLY INSTALLED AND CONFIGURED now waiting for reboot***', color=green, bold=True)
    reboot(wait=60)
    _stamp('**INSTANCE REBOOTED - try ssh or browser to %s' % HOST, color=green, bold=True)
    _stamp('Run "fab cleanup_files" to remove log files etc once the instance is checked and operational', color=cyan)
    _stamp('if assigning a DNS name change elastic ip on amazon manangement console, update DNS supplier, '
           'update server_config_secret.json then edit ~/.ssh/config and knownhosts files', color=cyan)
