from flask import Flask, render_template, url_for, redirect
from flask_restful import abort, Api, Resource, reqparse
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
from data.reviews import Review
from data.forms import *
import datetime


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'randomstring'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def main_page():
    return render_template('main_page.html', title='Главная')


@app.route('/feedback')
def feedback():
    session = db_session.create_session()
    reviews = session.query(Review).all()
    return render_template('feedback.html', title='Отзывы', reviews=reviews)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают')
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Пользователь с таким email уже существует')
        user = User()
        user.email = form.email.data
        user.set_password(form.password.data)
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/feedback')
        return render_template('login.html', title='Вход', form=form,
                               message='Неверный логин или пароль')
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/feedback')


def feel_db():
    session = db_session.create_session()
    for i in range(1, 6):
        review = Review()
        review.user_id = 1
        review.user_name = session.query(User).filter(User.id == 1).first().name
        review.user_surname = session.query(User).filter(User.id == 1).first().surname
        review.rating = i
        review.content = 'Lorem ipsum dolor sit amet consectetur, adipisicing elit. Quisquam ipsam fugiat natus ' \
                         'tempora molestias illo quis provident quod, maiores doloremque?'
        review.date = datetime.date.today()
        session.add(review)
    session.commit()


if __name__ == '__main__':
    app.template_folder = 'template'
    db_session.global_init('db/main_db.sqlite')
    app.run(port=5000, host='127.0.0.1')