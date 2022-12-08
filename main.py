import os
from flask_restful import abort, Api
from flask import Flask, request, session
# from data import category

from os import getenv
from werkzeug.exceptions import abort
from flask_bootstrap import Bootstrap
# import news_resources
from data import db_session
from data.users import User
# from data.goods import Goods
# from data.category import Category
# from forms.goods import GoodsForm
from forms.index import IndexForm
from forms.user import RegisterForm, LoginForm, EditEmailForm, EditPhoneForm, EditPasswordForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import redirect, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static")

api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = getenv('SECRET_KEY')

Bootstrap(app)

@app.route("/")
def index():
    form = IndexForm()
    # if form.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     goods = db_sess.query(Goods).filter(Goods.title == form.title.data.lower(),
    #                                         Goods.category == form.category.data).all()
    #
    #     return render_template("index.html", news=goods, title="Авито2.0", form=form)
    # db_sess = db_session.create_session()
    # goods = db_sess.query(Goods)
    return render_template("index.html", title="Cases", form=form)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        session['phone'] = form.phone.data
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                form=form,
                                message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if db_sess.query(User).filter(User.phone == form.phone.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/office')
@login_required
def office():
    return render_template("office.html", title="Cases")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                           message="Неправильный логин или пароль",
                           form=form)
    return render_template('login.html', title='Авторизация', form=form)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

def main():
    db_session.global_init("db/avito.db")
    #add_category()
    app.run()


if __name__ == '__main__':
    main()
