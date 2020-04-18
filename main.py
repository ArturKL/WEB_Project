from flask import Flask, render_template, url_for
from flask_restful import abort, Api, Resource, reqparse
from data import db_session

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'randomstring'


@app.route('/')
def main_page():
    return render_template('main_page.html', title='Главная')


if __name__ == '__main__':
    app.template_folder = 'template'
    db_session.global_init('db/main_db.sqlite')
    app.run(port=5000, host='127.0.0.1')