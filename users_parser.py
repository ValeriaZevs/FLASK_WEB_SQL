from flask_restful.reqparse import RequestParser


parser = RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('email', required=True, type=int)
parser.add_argument('phone', required=True)
parser.add_argument('hashed_password', required=True)