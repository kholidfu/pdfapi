#!/usr/bin/bash

fab create_user:$1
fab create_key
fab install_packages
fab create_venv:$2
fab install_packages_venv:$2
fab upload_package:$3,$2
fab setup_nginx
fab run_the_site:$2
