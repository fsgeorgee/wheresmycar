# Dude where is my car?

Small little app to allow me to remember in which floor I parked my car :)

Using Flask to create a simple Restfull app. The app will store the location in a text file, so it's very simple, not multi-user.

# Pre-requisites

``` bash
pip install flask-restful
pip install uwsgi

sudo apt-get install uwsgi-plugin-python
sudo apt-get install uwsgi uwsgi-emperor
```

# Configuring NGINX

Edit NGINX configuration file:

``` bash
sudo vi /etc/nginx/sites-enabled/default 
```

To include:

``` bash
server {
    listen      80;
    server_name *your URL*;
    charset     utf-8;
    client_max_body_size 75M;

    location / { try_files $uri @yourapplication; }
    location @dudewheresmycar {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/dudewheresmycar/dudewheresmycar.sock;
    }    
}
``` 

# Configuring uWSGI

Create a new uWSGI configuration file /var/www/dudewheresmycar/dudewheresmycar.ini:

``` bash
[uwsgi]
#application's base folder
base = /var/www/demoapp

#python module to import
app = hello
module = %(app)

home = %(base)/venv
pythonpath = %(base)

#socket file's location
socket = /var/www/demoapp/%n.sock

#permissions for the socket file
chmod-socket    = 666

#the variable that holds a flask application inside the module imported at line #6
callable = app

#location of log files
logto = /var/log/uwsgi/%n.log
````

Then create a new directory for uwsgi log files, and change its owner to your user:

``` bash
sudo mkdir -p /var/log/uwsgi
sudo chown -R ubuntu:ubuntu /var/log/uwsgi
```

# Configuring uWSGI Emperor

uWSGI Emperor is responsible for reading configuration files and spawing uWSGI processes to execute them. 

Create a new upstart configuration file to execute emperor - /etc/init/uwsgi.conf:

``` bash
description "uWSGI"
start on runlevel [2345]
stop on runlevel [06]
respawn

env UWSGI=/var/www/demoapp/venv/bin/uwsgi
env LOGTO=/var/log/uwsgi/emperor.log

exec $UWSGI --master --emperor /etc/uwsgi/vassals --die-on-term --uid www-data --gid www-data --logto $LOGTO
```

Create a folder to hold the configuration and symlink the configuration file into it:

``` bash
sudo mkdir /etc/uwsgi && sudo mkdir /etc/uwsgi/vassals
sudo ln -s /var/www/demoapp/demoapp_uwsgi.ini /etc/uwsgi/vassals
```

Setting ownership:

``` bash
sudo chown -R www-data:www-data /var/www/demoapp/
sudo chown -R www-data:www-data /var/log/uwsgi/
```

Open up the uwsgi config file(/var/www/demoapp/demoapp_uwsgi.ini) and change the value of chmod-socket from 666 to 644:

``` bash
#permissions for the socket file
chmod-socket    = 644
```

# Running the app

Start both NGINX and uWSGI:

``` bash
sudo service nginx start
sudo service uwsgi start
```
