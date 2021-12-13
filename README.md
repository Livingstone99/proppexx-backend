
# PROPEXX API

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Raaxo-Synergy/Propex---Backend-API.git
$ cd Propex---Backend-API
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```


**Parse a .env (dotenv) file directly using BASH**
```sh
$ export $(egrep -v '^#' .env | xargs)
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

## Geodjango and PostGis setup
### PostGIS

First, we need to enable an extension called PostGIS on the database-end. This extension will be in charge to handle all the geospatial storage and requests.

and ensure postgis is installed in your local machine. if its not run

for macOS environment
```
$ brew install postgis
$ brew install gdal
$ brew install libgeoip
```
get the path for GDAL_LIBRARY_PATH
```
$ brew info gdal
```
add this to the enviromental virable
```
GDAL_LIBRARY_PATH=/usr/local/Cellar/gdal/3.3.2/lib/libgdal.dylib
```
do the same for geos
```
$ brew info geos
GEOS_LIBRARY_PATH=/usr/local/Cellar/geos/3.9.1/lib/libgeos_c.dylib
```

Connect to your database:
```
$ psql -h [database_hostname] -p [database_port] -U [database_user] -l
```
or
```
$ psql [database_hostname]
```

Then run the following:
```
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
Once pip has finished downloading the dependencies:
```
## for linux environment
add the following virable to local enviroment, 
if path is not found user '''whereis''' to get the exact place libgdal.so is located
```
 OSGEO4W_ROOT=/usr/lib/x86_64-linux-gnu/libgeos_c.so.1
 GEOS_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgeos_c.so.1
 GDAL_LIBRARY_PATH=/usr/lib/libgdal.so.26
 ```
sh (env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.


## Tests

To run the tests, cd into the directory where manage.py is:
```
sh
(env)$ python manage.py test propexx
```
## Celery and Redis setup
ensure redis is install on your os, for linus os, simply run this command on terminal
```
$ sudo apt-get install redis-server
```
fire up the server:
```
$ redis-server
```
You can test that Redis is working properly by typing this into your terminal:
```
$ redis-cli-ping
```
redis should reply  with PONG 

### django dependencies

install celery
```
$ pip install celery
$ pip freeze > requirements.txt
```

add redis as a dependency in the django Project:
```
$ pip install redis
$ pip freeze > requirements.txt
``` 
Test that the Celery worker is ready to receive tasks:
```
$ celery -A propexx worker -l info
```
Kill the process with CTRL-C. Now, test that the Celery task scheduler is ready for action:
```
$ celery -A propexx beat -l info
```

if you already have redis server running on the default port, and you consider it safe to kill the process run:

```
$ sudo service redis-server stop
```


