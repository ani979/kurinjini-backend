brew install python
sudo pip3.8 install virtualenv
xcode-select --install
brew install postgresql 
pip3.8 install -r requirements.txt 
python3 -m venv ~/localDocuments/personal/env 
source ~/localDocuments/personal/env/bin/activate
pip3.8 install django-ses

## DB
## Install Postgres. Check in google.
psql
sudo -u animeshshrivastava createuser postgres
ALTER USER postgres WITH PASSWORD '12345678';
ALTER USER postgres CREATEDB;
create database kurinjini;

## Migrate
python manage.py makemigrations

## Go to the dirctory mysite and do python3 manage.py runserver
python manage.py runserver

## A file base.py would be missing. Do let me know and i shall mail you that

## Now when you go to server login using SSH on EC2
sudo systemctl stop uwsgi
sudo systemctl restart uwsgi
sudo nginx -t && sudo systemctl restart nginx

## helper to know ports
lsof -i:8001
sudo nestat -lnp
