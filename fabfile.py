#!/usr/bin/env python

"""
What you need to run this:
1. zipped app/ run.py and uwsgi.ini
2. default file which contain nginx conf
3. id_rsa.pub to connect to server without password prompt
4. 
"""

# fabric thing
from fabric.api import *
from fabric.tasks import execute
from farmers import Farmers

f = Farmers()
env.hosts = [f.droplet_ip()]

# as root
def create_user():
    env.user = "root"
    run("adduser sopier")
    run("adduser sopier sudo")

def create_key():
    local("ssh-copy-id -i /home/banteng/.ssh/id_rsa.pub sopier@" \
          + f.droplet_ip())

def install_packages():
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    run("sudo apt-get install build-essential python-dev" \
        " python-pip nginx emacs24-nox")
    run("sudo pip install virtualenv")

def create_venv():
    """ tiap domain dibuatkan virtualenv sendiri2"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    run("virtualenv hotoid.com")

def install_packages_venv():
    """ install flask uwsgi unidecode"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    with lcd("/home/sopier/hotoid.com"):
        with path("/home/sopier/hotoid.com/bin/", behavior="prepend"):
            run("pip install flask uwsgi unidecode")

def upload_package():
    """upload folder app/ run.py and uwsgi.ini from localhost"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    local("scp /tmp/generic/hotoid.com.tar.gz sopier@" + f.droplet_ip() + ":")

    run("mv hotoid.com.tar.gz hotoid.com/")
    run("cd hotoid.com/ && tar zxvf hotoid.com.tar.gz")
    run("cd hotoid.com/ && rm hotoid.com.tar.gz")

def setup_nginx():
    """
    rm default
    cp default from localhost
    """
    env.user = "root"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    local("scp /tmp/default root@" + f.droplet_ip() + ":")
    run("rm /etc/nginx/sites-available/default")
    run("cp default /etc/nginx/sites/")

def run_the_site():
    """ run the site!"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    with lcd("/home/sopier/hotoid.com"):
        with path("/home/sopier/hotoid.com/bin/", behavior="prepend"):
            run("nohup uwsgi uwsgi.ini &")
