Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.6
* virtualenv + pip
* Git

eg, on Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update -y
    sudo apt-get install -y nginx git python3.6 python3.6-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME/USERNAME with, e.g., staging.my-domain.com/johndoe

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME/USERNAME with, e.g., staging.my-domain.com/johndoe

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
