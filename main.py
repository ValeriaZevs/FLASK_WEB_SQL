from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.orders import Orders
from data.login import LoginForm
from data.job_form import JobForm
from data.registration import RegisterForm
from data.department import Department, DepForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
#http://127.0.0.1:8080/login
#http://127.0.0.1:8080/for_admin2
#http://127.0.0.1:8080/add_job
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):  #функция для получения пользователя
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/for_admin")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("works_log.html", jobs=jobs, names=names)


@app.route('/add_job',  methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        job = Jobs(job=form.title.data, team_leader=form.team_leader.data, work_size=form.work_size.data,
                   collaborators=form.collaborators.data, is_finished=form.is_finished.data)
        db.add(job)
        db.commit()
        return redirect("/for_admin")
    return render_template('addjob.html', title='Adding a job', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def change_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            form.title.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
            db_sess.commit()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job:
            job.job = form.title.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/for_admin')
    return render_template('addjob.html', title='Aditing Job', form=form)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
        return redirect('/for_admin')
    return redirect('/for_admin')


@app.route("/for_admin2")
def index2():
    session = db_session.create_session()
    department = session.query(Department).all()
    return render_template("department_log.html", departments=department)


@app.route('/add_department',  methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepForm()
    if form.validate_on_submit():
        db = db_session.create_session()
        dep = Department(title=form.title.data, chief=form.team_leader.data, members=form.members.data,
                         email=form.email.data)
        db.add(dep)
        db.commit()
        return redirect("/for_admin2")
    return render_template('adddep.html', title='Adding a department', form=form)


@app.route('/department_change/<int:id>', methods=['GET', 'POST'])
@login_required
def department_change(id):
    form = DepForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep:
            form.title.data = dep.title
            form.team_leader.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
            db_sess.commit()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.team_leader.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/for_admin2')
    return render_template('adddep.html', title='Aditing Department', form=form)


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
        return redirect('/for_admin2')
    return redirect('/for_admin2')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация', form=form, message="Пароли не совпадают")
        db = db_session.create_session()
        if db.query(Orders).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(name=form.name.data, surname=form.surname.data, phone=form.phone.data, email=form.email.data)
        user.set_password(form.password.data)
        db.add(user)
        db.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():  #обработчик адреса /login
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect("/for_admin")
        return render_template('login.html', title='Авторизация', message="WRONG USER", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():  #мы «забываем» пользователя при помощи функции logout_user и перенаправляем его на главную страницу
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    db_session.global_init("db/users2.db")
    app.run(port=8080, host='127.0.0.1')