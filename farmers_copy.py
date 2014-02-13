#!/usr/bin/env python
# author: @sopier
"""
Steps
1. create droplet
satu droplet diisi 5 domain, berarti ketika add domain di DO, semua
dipointing ke IP droplet baru tersebut
2. pastikan di namecheap sudah dipointing ke dns digitalocean
3. setting server dan menghidupkan satu persatu domainnya
mulai tahap ini sebisa mungkin kita tidak hard login ke server, cukup dari
localhost controlnya :)
- copy-ssh-id dari local ke remote
- adduser
- install package required
- create virtualenv for each site in home folder
/home/sopier/selyrics.com
/home/sopier/soundrenalin.com
etc.

- setting nginx
remove /etc/nginx/sites-available/default dengan buatan sendiri dari localhost
- setting uwsgi
di localhost siapkan folder app/ run.py dan uwsgi.ini yang sudah di-compress
dengan format: example.com.tar.gz
- edit run.py nya

"""

from dop.client import Client
import urllib2
import sys

class Farmers(object):

    CLIENT_ID = 'your_client_id'
    API_KEY = 'your_api_key'

    def __init__(self):
        pass

    def create_droplet(self):
        """ step 1: creating droplet """
        client = Client(self.CLIENT_ID, self.API_KEY)
        droplet = client.create_droplet("test", 66, 1505699, 1)
        print droplet.to_json()['id']

    def droplet_ip(self):
        client = Client(self.CLIENT_ID, self.API_KEY)
        droplets = client.show_active_droplets()
        return [droplet.to_json() for droplet in droplets][-1]['ip_address']

    def add_domains(self):
        """ step 2: add domain to droplet """
        ip_address = self.droplet_ip()

        domains = [
            'www.soundrenalin.org',
            ]

        for domain in domains:
            urllib2.urlopen(
                "https://api.digitalocean.com/domains/new?client_id=" \
                + self.CLIENT_ID + "&api_key=" + self.API_KEY + "&name=" \
                + domain + "&ip_address=" + ip_address)

# setelah ini bisa berlanjut ke namecheap API

if __name__ == "__main__":
    f = Farmers()
    sys.stdout.write("preparing to create droplet...\n")
    f.create_droplet()
    sys.stdout.write("droplet successfully created!\n")
    print(f.droplet_ip())
    f.add_domains()
    
