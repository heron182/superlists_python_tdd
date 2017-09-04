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
`sed -e "s/SITENAME/staging.my-domain.com/g" -e "s/USERNAME/johndoe/g" \
    source/deploy_tools/nginx.tpl.conf | \
    sudo tee /etc/nginx/sites-available/staging.my-domain.com`

## Systemd service

* see gunicorn-systemd.template.service
* replace SITENAME/USERNAME with, e.g., staging.my-domain.com/johndoe
`sed -e "s/SITENAME/staging.my-domain.com/g" -e "s/USERNAME/johndoe/g" \
source/deploy_tools/gunicorn-systemd.tpl.service | \
sudo tee /etc/systemd/system/gunicorn-systemd.service`

## Folder structure:
Assume we have a user account at /home/username

/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
