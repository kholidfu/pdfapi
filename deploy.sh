#!/usr/bin/bash

fab create_user:"sopier"
fab create_key
fab install_packages
fab create_venv:"hotoid.com"
fab install_packages_venv:"hotoid.com"
fab upload_package:"hotoid.com.tar.gz","hotoid.com"
fab setup_nginx
fab run_the_site:"hotoid.com"
