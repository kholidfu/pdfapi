#!/usr/bin/env python
# author: @sopier

from dop.client import Client
import urllib2
import sys

class Farmers(object):

    CLIENT_ID = 'client_id'
    API_KEY = 'api_key'

    def __init__(self):
        pass

    def create_droplet(self, name):
        """ step 1: creating droplet """
        client = Client(self.CLIENT_ID, self.API_KEY)
        droplet = client.create_droplet(name, 66, 1505699, 1)
        print droplet.to_json()['id']

    def droplet_ip(self):
        client = Client(self.CLIENT_ID, self.API_KEY)
        droplets = client.show_active_droplets()
        return [droplet.to_json() for droplet in droplets][-1]['ip_address']

    def add_domain(self, domain):
        """ step 2: add domain to droplet """
        ip_address = self.droplet_ip()

        urllib2.urlopen(
            "https://api.digitalocean.com/domains/new?client_id=" \
            + self.CLIENT_ID + "&api_key=" + self.API_KEY + "&name=" \
            + domain + "&ip_address=" + ip_address)


if __name__ == "__main__":
    f = Farmers()
    sys.stdout.write("preparing to create droplet...\n")
    f.create_droplet(sys.argv[1])
    sys.stdout.write("droplet successfully created!\n")
    f.add_domains(sys.argv[2])
    sys.stdout.write("all domains added...\n")

# setelah ini bisa berlanjut ke namecheap API
