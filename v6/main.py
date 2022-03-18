from flask import Flask, render_template, redirect, request, make_response, jsonify, g
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.add_jobs import AddJobs
from forms.login import LoginForm
from forms.user import RegisterForm
from v6._rest.jobs_api import JobListRes, JobRes
from v6._rest.user_resource import UsersResource, UsersListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app, prefix='/api/v2')
api.catch_all_404s = True
api.add_resource(JobListRes, '/jobs')
api.add_resource(JobRes, '/jobs/<int:job_id>')
api.add_resource(UsersResource, '/users/<int:user_id>')
api.add_resource(UsersListResource, '/users')


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run(debug=True)


@app.before_request
def before_request():
    g.db_sess = db_session.create_session()


@app.teardown_request
def teardown_request(teardown):
    g.db_sess.close()


@login_manager.user_loader
def load_user(user_id):
    return g.db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = g.db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route("/index")
@login_required
def index():
    jobs = g.db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs)


@app.route("/delete_job/<int:id_job>")
@login_required
def del_job(id_job):
    job = g.db_sess.query(Jobs).filter(Jobs.id == id_job).first()
    g.db_sess.delete(job)
    g.db_sess.commit()
    return redirect('/index')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = AddJobs()
    if form.validate_on_submit():
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start.data
        job.end_date = form.end.data
        job.is_finished = form.finish.data
        job.team_leader = form.leader.data
        g.db_sess.add(job)
        g.db_sess.commit()
        return redirect('/index')
    return render_template('add_jobs.html', form=form)


@app.route('/edit_job/<int:id_job>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id_job):
    form = AddJobs()
    if request.method == "GET":
        job = g.db_sess.query(Jobs).filter(Jobs.id == id_job).first()
        form.job.data = job.job
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.start.data = job.start_date
        form.end.data = job.end_date
        form.finish.data = job.is_finished
        form.leader.data = job.team_leader
    if form.validate_on_submit():
        job = g.db_sess.query(Jobs).filter(Jobs.id == id_job).first()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = form.start.data
        job.end_date = form.end.data
        job.is_finished = form.finish.data
        job.team_leader = form.leader.data
        g.db_sess.commit()
        return redirect('/index')
    return render_template('add_jobs.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    users = g.db_sess.query(User)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        if g.db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        g.db_sess.add(user)
        g.db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form, users=users)


@app.errorhandler(404)
def not_found404(error):
    return make_response(jsonify({'error': 'main. Not found'}), 404)


@app.errorhandler(401)
def not_found(error):
    msg = 'Ошибка'
    if "401" in str(error):
        msg = 'Пользователь не авторизован (401)'
    elif "404" in str(error):
        msg = 'Страница не найдена (404)'
    return render_template("base.html", message=msg)


if __name__ == '__main__':
    main()
