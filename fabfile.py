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

def upload_package(package, domain):
    """upload folder app/ run.py and uwsgi.ini from localhost"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    local("scp " + package + " sopier@" + f.droplet_ip() + ":")

    run("mv " + package + " " + domain + "/")
    run("cd " + domain + " && tar zxvf " + package)
    run("cd " + domain + " && rm " + package)

def setup_nginx():
    """
    rm default
    cp default from localhost
    """
    env.user = "root"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    local("scp default root@" + f.droplet_ip() \
          + ":/etc/nginx/sites-available/default")
    run("service nginx restart")

def run_the_site(domain):
    """ run the site!"""
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    local("scp supervisord.conf sopier@" + f.droplet_ip() + ":")
    run("sudo supervisord -c supervisord.conf")

"""
todo:
1. coba supervisord pake yang inside virtualenv
2. conf nya pake yang didalam home/sopier/domain aja
"""
