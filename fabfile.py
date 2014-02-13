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
    pass

def install_packages_venv():
    """ install flask uwsgi unidecode"""
    pass

def edit_run():
    """ edit the run.py file"""
    pass

def create_uwsgi():
    """ create uwsgi.ini"""
    pass

def setup_nginx():
    """
    rm default
    cp default from localhost
    """
    pass

def run_the_site():
    """ run the site!"""
    pass
