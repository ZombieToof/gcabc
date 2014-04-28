gcabc is a prototype to implement global conflict's campaign management 
system ABC (Army Base Camp) in django and integrate it with phpBB. ABC
is used to organize Battlefield 4 tournaments where two big armies compete
in a risk like campaign system.

gcabc is an unfinshed pre-alpha prototype to see how fast it can be build
in django and if it is beneficial in the end.

To implement ABC we build basically the same database structure used in the
original ABC with django models, use the same database phpBB uses and
couple it through django-phpBB3.


Manual Installation
===================

The short road to a complete dev envionment is to use vagrant with the
configuration from https://github.com/ZombieToof/gcdev which gives you a
virtual machine with ubuntu 14.04 / phpBB / GCWeb (ABC in php integrated
with phpBB) and this project.

Create a virtual env and install Django 1.7. Note that we have to use 
Python 2.7 cause the default mysql library is not Python 3 ready yet,
and you can get only an alpha prototype, or the installation is cumbersome.

We install a virtualenv here and with the `--no-site-packages` option.
So we have access to python's stdlib, but not other globally installed 
python modules. So we need some packages to build Pillow and
MYSQL-python inside our virualenv.::

  # short cut
  sudo apt-get build-dep python-mysql
  sudo apt-get build-dep python-pil

  # long version (Debian 7/Ubuntu 12.04)
  sudo apt-get install build-essential
  sudo apt-get install libmysqlclient-dev
  sudo apt-get install python-dev python-setuptools
  sudo apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk


Now we can install our virtualenv::

  virtualenv --no-site-package /srv/gcdjango --python=/usr/bin/python-2.7
  cd /srv/gcdjango
  . bin/activte
  pip install Pillow
  pip install MYSQL-python
  pip install https://www.djangoproject.com/download/1.7b2/tarball


Clone this project into a subdirectory::

  git clone FIXME gcabc
  cd gcabc

Now you have to edit the database settings. Since we will have to access
the phpbb database tables (work in progress) and want to use foreign keys
to the phpbb users table it needs to be the phpbb database. So go on and
edit gcabc/settings.py and set the correct database and the phpbb table 
prefix.
If the database, db user and password are all 'phpbb' this looks like::


  PHPBB_TABLE_PREFIX = "phpbb_"

  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'phpbb',
        'USER': 'phpbb',
        'PASSWORD': 'phpbb',
    }

To create the database tables for the django ABC you run the django
migrations and then run the development server::

  python manage.py migrate
  python manage.py runserver
