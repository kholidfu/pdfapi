# fabric thing
from fabric.api import *
from fabric.tasks import execute
from farmers import Farmers

env.hosts = [f.droplet_ip()]
env.user = "root"
#env.key_filename = "/home/banteng/.ssh/id_rsa"

# as root
def create_user():
    run("adduser sopier")
    run("adduser sopier sudo")

def install_packages():
    run("apt-get install build-essential python-dev python-pip nginx")
    run("pip install virtualenv")

# as user
# env.user = "sopier"

def create_key():
    local("ssh-copy-id -i /home/banteng/.ssh/id_rsa.pub sopier@" \
          + f.droplet_ip())


execute(create_user)
#execute(install_packages)
#excute(create_key)
