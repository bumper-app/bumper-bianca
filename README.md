python-package-boilerplate
==========================

[![Build Status](https://travis-ci.org/bumper-app/bumper-bianca.png?branch=master)](https://travis-ci.org/bumper-app/bumper-bianca)
[![Requires.io](https://requires.io/github/bumper-app/bumper-bianca/requirements.svg?branch=master)](https://requires.io/github/bumper-app/bumper-bianca/requirements?branch=master)

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

###First-Time Database Setup
Set up the database for the first time by running `python script.py initDb`

##Usage
In a terminal, type `nohup python script.py & ' to start the code repo analyzer and run it in the background.
