Installation
============

Create a virtual env and install Django 1.7. Note that we are on Python 3::

  virtualenv --no-site-package /srv/gcdjango --python=/usr/bin/python-3.3
  cd /srv/gcdjango
  . bin/activte
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
