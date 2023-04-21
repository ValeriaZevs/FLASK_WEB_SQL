import flask
from flask import jsonify
from data import db_session
from data.users import User
from flask import request
from requests import get, post
#http://127.0.0.1:8080/api/users
#http://127.0.0.1:8080/api/users/1


blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_news():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'surname', 'email', 'phone', 'hashed_password'))
                 for item in users]
        }
    )



@blueprint.route('/api/users/<int:id>')
def get_news_id(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter(User.id == id).first()
    if not users:
        return jsonify({'error': 'Not found'})
    else:
        return jsonify(
            {
                'users': users.to_dict(only=('id', 'name', 'surname', 'email', 'phone', 'hashed_password'))
            }
        )


@blueprint.route('/api/users', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'name', 'surname', 'email', 'phone', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user_has = db_sess.query(User).filter(User.id == request.json['id']).first()
    if user_has:
        return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        email=request.json['email'],
        phone=request.json['phone'],
        hashed_password=request.json['hashed_password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def delete_job(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:id>', methods=['PUT'])
def change_job(id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(id)
    if not users:
        return jsonify({'error': 'Not found'})
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'name', 'surname', 'email', 'phone', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    user2 = db_sess.query(User).get(request.json['id'])
    if user2 and user2 != users:
        return jsonify({'error': 'Id already exists'})
    users.id = request.json['id']
    users.name = request.json['name']
    users.surname = request.json['surname']
    users.email = request.json['email']
    users.phone = request.json['phone']
    users.hashed_password = request.json['hashed_password']
    db_sess.commit()
    return jsonify({'success': 'OK'})

#print(get('http://127.0.0.1:8080/api/jobs').json())