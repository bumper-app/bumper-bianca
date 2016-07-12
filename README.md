python-package-boilerplate
==========================

[![Build Status](https://travis-ci.org/mtchavez/python-package-boilerplate.png?branch=master)](https://travis-ci.org/mtchavez/python-package-boilerplate)
[![Requires.io](https://requires.io/github/mtchavez/python-package-boilerplate/requirements.svg?branch=master)](https://requires.io/github/mtchavez/python-package-boilerplate/requirements?branch=master)

Boilerplate for a Python Package

## Package

Basic structure of package is

```
├── README.md
├── packagename
│   ├── __init__.py
│   ├── packagename.py
│   └── version.py
├── pytest.ini
├── requirements.txt
├── setup.py
└── tests
    ├── __init__.py
    ├── helpers
    │   ├── __init__.py
    │   └── my_helper.py
    ├── tests_helper.py
    └── unit
        ├── __init__.py
        ├── test_example.py
        └── test_version.py
```

## Requirements

Package requirements are handled using pip. To install them do

```
pip install -r requirements.txt
```

## Tests

Testing is set up using [pytest](http://pytest.org) and coverage is handled
with the pytest-cov plugin.

Run your tests with ```py.test``` in the root directory.

Coverage is ran by default and is set in the ```pytest.ini``` file.
To see an html output of coverage open ```htmlcov/index.html``` after running the tests.

## Travis CI

There is a ```.travis.yml``` file that is set up to run your tests for python 2.7
and python 3.2, should you choose to use it.


Ingests and analyzes code repositories

##Installation
1. Clone this repository in to an empty directory
2. Copy the `./config.example.json` to `./config.json` and change the
the configurations. All fields are required.

Db: information relating to your postgresql database setup
logging: information about how to write logging information
gmail: gmail account to be used to send cas notifications
repoUpdates: how often repositories should be updated for new commits
system: how many worker threads the cas system can use to analyze and ingest repos.

###Dependencies
Additional Instructions are available in SETUP.md
* Python  >= 3.3
* Pip for Python Version > 3.3
* Git > 1.7
* R
* python-dev
* rpy2
* requests
* dateutil
* sqlalchemy
* py-postgresql
* GNU grep
* MonthDelta

###Setting up python3.3 virtual env on Fedora

    sudo yum install wget R python3-devel readline-devel
    
    wget https://bootstrap.pypa.io/ez_setup.py
    sudo python3 ez_setup.py
    
    sudo python3 -m easy_install pip
    sudo python3 -m easy_install virtualenv

virtualenv --no-site-packages --distribute -p /usr/bin/python3 ~/.virtualenvs/pywork3

Now, we are finally ready to set up our virtual environment:

    virtualenv -p /usr/bin/python3 ~/pyVirtual/cas

To activate the virtual env:

    source ~/pyVirtual/cas/bin/activate

    pip install sqlalchemy
    pip install py-postgresql
    pip install requests
    pip install python-dateutil
    pip install http://pypi.python.org/packages/source/M/MonthDelta/MonthDelta-1.0b.tar.bz2
    

###Setting up python3.3 virtual env on Ubuntu
* Assumes you are working on Ubuntu 12.04

Install python3.3 using the deadsnakes PPA:

```
sudo apt-get install python-software-properties
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.3
```

Version 1.7.1.2 of virtual env that comes with Ubuntu 12.04 is not compatibale with python3.3.
Therefore, we must installa new version so that we can setup a working virutal environment. First,
you must uninstall the current python-virtualenv:

```
sudo apt-get remove python-virtualenv
```

Next, install the latest easy_install:

```
wget http://peak.telecommunity.com/dist/ez_setup.py
sudo python ez_setup.py
```

Next, install pip and the virtualenv:

```
sudo easy_install pip
sudo pip install virtualenv
virtualenv --no-site-packages --distribute -p /usr/bin/python3.3 ~/.virtualenvs/pywork3
```

By default, typically we don't have the python-dev available for python3 on Ubuntu after setting up a new
virtual environment for it and so have to install it as it's a dependency for rpy2. Install this with apt-get:

```
sudo apt-get install python3.3-dev
```

Now, we are finally ready to set up our virtual environment:

```
virtualenv -p /usr/bin/python3.3 /path/to/new/virtual/environment
```

To activate the virtual env:

```
source /path/to/new/virtual/environemnt/bin/activate
```

Type `deactiviate` to exit the virtual env

####Installing rpy2
* Assumes you are working on Ubuntu 12.04 and python 3.3

Getting rpy2 to work can be a bit tricky. First, make sure R is installed. To do this, first
get the repository SSL key and import it to apt by doing

  ```
  gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
  gpg -a --export E084DAB9 | sudo apt-key add -
  ```

Then, Edit the list of sources `gksudo gedit /etc/apt/sources.list` and add the following repo at the bottom:`deb http://cran.ma.imperial.ac.uk/bin/linux/ubuntu precise/`

Finally, we can install R by running the following commands:

  ```
  sudo apt-get update
  sudo apt-get install r-base
  ```

Now we are ready to install rpy2. Make sure python version 3 or greater is in use (3.2 is not compatibale, however), such as by using a virtualenv and run

```
pip install rpy2
```

####Additional Pip Packages
Install the following packages by doing `pip install `  and then the package
name. Make sure you are using python3, such as using a virtualenv if using Ubuntu.

* SQL Alchemy (sqlalchemy)
* Py-PostgreSQL (py-postgresql)
* requests (requests)
* python-dateutil (python-dateutil)

To install the MonthDelta package, simply do: `pip install http://pypi.python.org/packages/source/M/MonthDelta/MonthDelta-1.0b.tar.bz2`

###First-Time Database Setup
Set up the database for the first time by running `python script.py initDb`

##Usage
In a terminal, type `nohup python script.py & ' to start the code repo analyzer and run it in the background.
