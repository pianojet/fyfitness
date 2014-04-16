fyfitness
=========

apt-get install apache2 apache2-mpm-worker libapache2-mod-wsgi python-pip git mercurial mysql-client libmysqlclient-dev python-dev build-essential graphviz libgraphviz-dev pkg-config sensible-mda libxml2-dev libxslt1-dev mysql-server

pip install virtualenv

cd /opt/git

git clone https://github.com/pianojet/fyfitness.git

cd fyfitness

./bootstrap.py

source venv/bin/activate

export DJANGO_SETTINGS_MODULE=settings.development

pip install -r requirements.debug.txt

sudo ln -s /opt/git/fyfitness/conf/apache/vhost.development.conf /etc/apache2/sites-available/fyfitness_development

sudo a2ensite fyfitness_development

#<run mysql client>
>>>
CREATE USER 'fyfitness'@'localhost' IDENTIFIED BY 'pass123';
GRANT ALL PRIVILEGES ON * . * TO 'fyfitness'@'localhost';
FLUSH PRIVILEGES;
create database fyfitness;
<<<

./manage.py syncdb

./manage.py migrate

# can use runserver:
./manage.py runserver solicon.me:8000