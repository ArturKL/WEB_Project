import os
from flask import Flask
from flask_restful import abort, Api, Resource, reqparse
from data import db_session

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'randomstring'

if __name__ == '__main__':
    app.template_folder = 'template'
    db_session.global_init('db/main_db.sqlite')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)