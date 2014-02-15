#!/usr/bin/env python
# author: @sopier
"""
Automate flask app deployment

What you need to run this:
1. zipped app/ run.py and uwsgi.ini => format domain.xxx.tar.gz
2. "default" file which contain all sites conf
3. id_rsa.pub to connect to server without password prompt
4. supervisord.conf latest version

"""

# fabric thing
from fabric.api import *
from fabric.tasks import execute
from farmers import Farmers

f = Farmers()
env.hosts = [f.droplet_ip()]
droplet_ip = env.hosts[0]

def add_domain(site):
    """ adding domain to DO"""
    f.add_domain(site)

def create_user():
    env.user = "root"
    run("adduser sopier")
    run("adduser sopier sudo")

def create_key():
    """ delete old keys and generate new one"""
    local("> ~/.ssh/known_hosts")
    local("ssh-copy-id -i /home/banteng/.ssh/id_rsa.pub sopier@" \
          + droplet_ip)

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
    local("scp " + package + " sopier@" + droplet_ip + ":")

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
    local("scp default root@" + droplet_ip \
          + ":/etc/nginx/sites-available/default")
    sudo("sed -i 's/.*64.*/server_names_hash_bucket_size 64;/' /etc/nginx/nginx.conf")
    sudo("/etc/init.d/nginx restart")

def set_supervisor(domain):
    """ setup for supervisor """
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    local("scp run.py sopier@" + droplet_ip + ":/home/sopier/" + domain)
    local("scp supervisord.conf sopier@" + droplet_ip + ":")

def run_site():
    """ run the site """
    env.user = "sopier"
    env.key_filename = "/home/banteng/.ssh/id_rsa"
    try:
        sudo("pkill supervisord")
    except:
        pass
    sudo("supervisord -c supervisord.conf")

def setup_server():
    create_user()
    create_key()
    install_packages()

def deploy_site(site):
    add_domain("www." + site)
    create_venv(site)
    install_packages_venv(site)
    upload_package(site + ".tar.gz", site)
    setup_nginx()
    set_supervisor(site)
    run_site()
