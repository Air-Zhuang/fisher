from flask import Flask
from flask_login import LoginManager   #专为flask定制的
from app.models.base import db

login_manager=LoginManager()

def create_app():
    app=Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    login_manager.init_app(app)                     #初始化LoginManager
    login_manager.login_view='web.login'            #指定cookie不通过时重定向的页面
    login_manager.login_message='请先登录或注册'     #不通过验证重定向之后闪现的消息
    db.init_app(app)
    db.create_all(app=app)
    return app

def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)