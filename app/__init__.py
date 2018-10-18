from flask import Flask
from flask_login import LoginManager   #专为flask定制的
from app.models.base import db
from flask_mail import Mail

login_manager=LoginManager()                        #flask_login初始化
mail=Mail()                                         #flask_mail初始化

def create_app():
    app=Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    login_manager.init_app(app)                     #初始化LoginManager
    login_manager.login_view='web.login'            #指定cookie不通过时重定向的页面
    login_manager.login_message='请先登录或注册'     #未登录状态重定向到login界面之后flask-login会默认闪现一条消息消息

    mail.init_app(app)                              #注册flask_mail插件

    db.init_app(app)                                #注册flask-SQLAlchemy插件
    db.create_all(app=app)                          #创建表
    return app

def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)