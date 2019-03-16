"""__author__ = 蒲金彪"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 创建文章和用户的中间表：评论表
a_u = db.Table('a_u',
               db.Column('id', db.Integer, primary_key=True, autoincrement=True),
               db.Column('create_time', db.DateTime, default=datetime.day),
               db.Column('comments', db.Text, nullable=False),
               db.Column('a_id', db.Integer, db.ForeignKey('article.id'), nullable=True, primary_key=True),
               db.Column('u_id', db.Integer, db.ForeignKey('user.id'), nullable=True, primary_key=True))


# 创建一个用户模型
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_delete = db.Column(db.Boolean, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    art = db.relationship('Article', secondary=a_u, backref='users')

    def save(self):
        db.session.add(self)
        db.session.commit()


# 创建一个文章类型类
class Article_type(db.Model):
    __tablename__ = 'art_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(10), nullable=False, unique=True)
    arts = db.relationship('Article', backref='tp')

    def save(self):
        db.session.add(self)
        db.session.commit()


# 创建一个文章类
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False, unique=True)
    desc = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    type = db.Column(db.Integer, db.ForeignKey('art_type.id'))
    is_publish = db.Column(db.Boolean, default=0)
    max_num = db.Column(db.Integer, default=0)







