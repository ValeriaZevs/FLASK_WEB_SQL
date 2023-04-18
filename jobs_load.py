from flask import Flask
from data import db_session
from data.department import Department

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/departments.db")
    # app.run()
    session = db_session.create_session()
    dep = Department()
    dep.title = "Geo"
    dep.chief = 1
    dep.members = '2'
    dep.email = 'department@mail.ru'
    session.commit()



if __name__ == '__main__':
    main()