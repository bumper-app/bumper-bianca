BIANCA
==========================

[![Build Status](https://travis-ci.org/bumper-app/bumper-bianca.png?branch=master)](https://travis-ci.org/bumper-app/bumper-bianca)

[![Documentation Status](https://readthedocs.org/projects/bumper-bianca/badge/?version=latest)](http://bumper-bianca.readthedocs.org/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/pyversions/bumper-bianca.svg)](https://pypi.python.org/pypi/bumper-bianca/1.0.0)
[![GitHub tag](https://img.shields.io/github/tag/ereOn/bumper-bianca.svg)](https://github.com/ereOn/bumper-bianca)
[![PyPi version](https://img.shields.io/pypi/v/bumper-bianca.svg)](https://pypi.python.org/pypi/bumper-bianca/1.0.0)
[![PyPi downloads](https://img.shields.io/pypi/dm/bumper-bianca.svg)](https://pypi.python.org/pypi/bumper-bianca/1.0.0)

[![Requires.io](https://requires.io/github/bumper-app/bumper-bianca/requirements.svg?branch=master)](https://requires.io/github/bumper-app/bumper-bianca/requirements?branch=master)


## Dependencies

External depedencies are Postgresql & R


  ```
  gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9
  gpg -a --export E084DAB9 | sudo apt-key add -
  ```

Then, Edit the list of sources `gksudo gedit /etc/apt/sources.list` and add the following repo at the bottom:`deb http://cran.ma.imperial.ac.uk/bin/linux/ubuntu precise/`

Finally, we can install R by running the following commands:

  ```
  sudo apt-get update
  sudo apt-get install r-base postgresql postgresql-contrib
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


##Installation
1. Clone this repository in to an empty directory
2. Copy the `./config.example.json` to `./config.json` and change the
the configurations. All fields are required.

Db: information relating to your postgresql database setup
logging: information about how to write logging information
gmail: gmail account to be used to send cas notifications
repoUpdates: how often repositories should be updated for new commits
system: how many worker threads the cas system can use to analyze and ingest repos.

###First-Time Database Setup
Set up the database for the first time by running `python script.py initDb`

##Usage
In a terminal, type `nohup python script.py & ' to start the code repo analyzer and run it in the background.
