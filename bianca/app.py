from flask import Flask, jsonify, request, abort, make_response
from analyzer.analyzer import *
from ingester.ingester import *
from orm.repository import *
import calendar # to convert datetime to unix time
from caslogging import logging
from queue import *
import threading
import time
from monthdelta import *

app = Flask(__name__)
session = Session()

@app.route('/')
def index():
    return "Nothing to see"

@app.route('/api/v1.0/repos', methods=['POST'])
def create_repo():
    if not request.json or not 'url' in request.json:
        abort(400)

    repos = (session.query(Repository) 
	.filter_by(url = request.json['url'])
	.all())

    repo = None

    print(request.json['url']);

    if len(repos) == 0:
        print("hi")
        repo = Repository(url=request.json['url'])
        session.add(repo)
        session.commit()
    else:
        repo = repos[0]

    return jsonify(repo.as_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)