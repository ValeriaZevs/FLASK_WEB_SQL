import flask
from flask import jsonify
from data import db_session
from data.users import User
from flask import request
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, render_template, redirect, request
from data.users_parser import *

app = Flask(__name__)
api = Api(app)


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(only=('id', 'name', 'surname', 'email', 'phone', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'surname', 'email', 'phone', 'hashed_password')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            id=args['id'],
            name=args['name'],
            surname=args['surname'],
            email=args['email'],
            phone=args['phone'],
            hashed_password=args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})








