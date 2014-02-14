#!/usr/bin/env python
# author: @sopier
"""
Automate server deployment

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

def create_user(user):
    env.user = "root"
    run("adduser " + user)
    run("adduser " + user + " sudo")

def create_key():
    local("ssh-copy-id -i /home/banteng/.ssh/id_rsa.pub sopier@" \
          + f.droplet_ip())

def install_packages():
    env.user = "root"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    run("apt-get install build-essential python-dev" \
        " python-pip nginx emacs24-nox && pip install virtualenv")

def create_venv(domain):
    """ tiap domain dibuatkan virtualenv sendiri2, misal example.com"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    run("virtualenv " + domain)

def install_packages_venv(domain):
    """ install flask uwsgi unidecode"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    with lcd("/home/sopier/" + domain):
        with path("/home/sopier/" + domain + "/bin/", behavior="prepend"):
            run("pip install flask uwsgi unidecode")

def upload_package(f, domain):
    """upload folder app/ run.py and uwsgi.ini from localhost"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    local("scp /tmp/generic/" + f + " sopier@" + f.droplet_ip() + ":")

    run("mv " + f + " " + domain + "/")
    run("cd " + domain + " && tar zxvf " + f)
    run("cd " + domain + " && rm " + f)

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

def run_the_site(domain):
    """ run the site!"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    with lcd("/home/sopier/" + domain):
        with path("/home/sopier/" + domain + "/bin/", behavior="prepend"):
            run("nohup uwsgi uwsgi.ini &")
