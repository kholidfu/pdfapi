#!/usr/bin/env python
# author: @sopier
"""
Automate flask app deployment

What you need to run this:
1. zipped app/ run.py and uwsgi.ini
2. default file which contain nginx conf
3. id_rsa.pub to connect to server without password prompt
4. supervisord.conf file
5. bikin run.py baru dengan if __name__
"""

# fabric thing
from fabric.api import *
from fabric.tasks import execute
from farmers import Farmers

f = Farmers()
env.hosts = [f.droplet_ip()]

def create_user():
    env.user = "root"
    run("userdel -r sopier")
    run("adduser sopier")
    run("adduser sopier sudo")

def create_key():
    """ delete old keys and generate new one"""
    local("> ~/.ssh/known_hosts")
    local("ssh-copy-id -i /home/banteng/.ssh/id_rsa.pub sopier@" \
          + f.droplet_ip())

def install_packages():
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    run("sudo apt-get install build-essential python-dev" \
        " python-pip nginx emacs24-nox")
    run("sudo pip install virtualenv supervisor")

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
            run("pip install flask uwsgi unidecode pymongo")

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
    sudo("/etc/init.d/nginx restart")

def set_supervisor(domain):
    """ setup for supervisor """
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    local("scp supervisord.conf run.py sopier@" + f.droplet_ip() + ":/home/sopier/" + domain)

def run_site(domain):
    """ run the site """
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    run("cd /home/sopier/" + domain + " && sudo supervisor "\
        " supervisor stop && sudo supervisor start")

def setup_server():
    create_user()
    create_key()
    install_packages()

def deploy_site(site):
    create_venv(site)
    install_packages_venv(site)
    upload_package(site + ".tar.gz", site)
    setup_nginx()
    set_supervisor(site)
    run_site(site)
