"""__author__ = 蒲金彪"""
import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.models import db
from back.views import back_blue
from web.views import web_blue

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pjbxhqs7741743@47.101.207.205/MyBlog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = '3434545454556jfgrgjifgirgkj'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
Session(app)

db.init_app(app)
app.register_blueprint(blueprint=web_blue, url_prefix='/web')
app.register_blueprint(blueprint=back_blue, url_prefix='/back')
manage = Manager(app)


if __name__ == '__main__':
    manage.run()



