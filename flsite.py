import sqlite3
import os
from database.db import FDataBase
from jinja2 import Environment, FileSystemLoader
from flask import (Flask, flash, render_template, request,
                   redirect, url_for, get_flashed_messages,
                   make_response, session, abort, g)
from validate import validate_post

# конфигурация
SECRET_KEY = "3&t72u%*23a$59#1f%8hs*$%hre#@%"
DEBUG = True
DATABASE = '/tmp/database/flsite.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path,
                                             'database/flstite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    # Вспомогательная функция для создания таблиц БД
    db = connect_db()
    with app.open_resource('database/sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html',
                           menu=dbase.getMenu(),
                           posts=dbase.getPostsAnnounce())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/page404.html',
                           title='Страница не найдена')


@app.errorhandler(401)
def denied_access(error):
    return render_template('errors/page401.html',
                           title='Неавторизованный пользователь')


# @app.route('/about')
# def about():
#     return render_template('about.html',
#                            title='О сайте',
#                            menu=menu)


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        name = request.form['name']
        post = request.form['post']
        url = request.form['url']
        if validate_post(name, post):
            res = dbase.addPost(name, post, url)
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка.Увеличьте количество символов',
                  category='error')

    return render_template('posts/add_post.html',
                           menu=dbase.getMenu(),
                           title="Добавление статьи")


@app.route("/post/<alias>")
def show_post(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('posts/post.html', menu=dbase.getMenu(),
                           title=title,
                           post=post)


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():

#     if request.method == "POST":
#         if len(request.form['username']) > 2:
#             flash('Сообщение отправлено', category='success')
#         else:
#             flash('Ошибка отправки', category="error")
#     return render_template('contact.html',
#                            title="Обратная связь",
#                            menu=dbase.getMenu())


# @app.route('/profile/<username>')
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f'Профиль пользователя: {username}'


# @app.route('/login', methods=['GET', 'POST'])
# def log_in():
#     if "userLogged" in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == 'krushovice' and request.form['psw'] == '256':
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#     return render_template('login.html', title='Авторизация')


if __name__ == '__main__':
    app.run(debug=True)
