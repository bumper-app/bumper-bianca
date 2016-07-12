"""
file: config.py
author: Ben Grawi <bjg1568@rit.edu>
date: November 2013
description: Reads the config.json info into a varible
"""
import json
#from StringIO import StringIO
import os

config = json.load(open('./config.json'))

# Defining default repository path if not specified
if config['repo_location']['location'] and config['repo_location']['location'] != "":
    REPO_DIRECTORY = config['repo_location']['location'] + "/"
else:
    REPO_DIRECTORY = os.path.join(os.path.dirname(__file__), "ingester/CASRepos/git/")
