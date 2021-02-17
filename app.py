import sys, json
from flask import Flask, redirect, request, url_for, jsonify
import requests, logging
import DB

app = Flask(__name__)

@app.route('/')
def home():
    app.logger.info('home')
    return "Hello World"


@app.route('/user', methods=['POST']
def get_user():
    req = request.get_json()

    DB.create_user() # email, name, interests
    return 0


@app.route('/login', methods=['GET']
def login():
    req = request.get_json()

    ret = DB.login_user(req['email'])

    return jsonify(ret)


@app.route('/room/create', methods=['POST'])
def get_data():
    req = request.get_json()
    # update db
    logging.info("update data")
    logging.info(req)

    # category, name, captain_email, captain_name, max_penalty, description=None
    DB.create_room()

    return 0


@app.route('/room/enter', methods=['POST'])
def enter_room():
    req = request.get_json()

    # category, name, crew_email, crew_name
    DB.enroll_room()

    return 0


@app.route('/room/recommands', methods=['GET'])
def recommand_rooom():
    req = request.get_json()

    # email
    DB.recommend_room()

    return 0


@app.route('/room/close', methods=['PUT'])
def close_room():
    req = request.get_json()

    # category, name
    DB.close_room()

    return 0


@app.route('/room/adjust', methods=['PUT'])
def adjust_room():
    req = request.get_json()

    # category, name, progress
    DB.adjust_progress()

    return 0


@app.route('/room/todo/add', methods=['POST'])
def add_todo():
    req = request.get_json()

    # category, name, email, todo
    DB.add_todo()

    return 0

@app.route('/room/todo/clear', methods=['PUT'])
def clear_todo():
    req = request.get_json()

    # category, name, email, todo
    DB.clear_todo()

    return 0



@app.route('', methods=[])

if __name__ == "__main__":
    logging.info("start")
    app.run(host='0.0.0.0', port='5000', debug=True)
