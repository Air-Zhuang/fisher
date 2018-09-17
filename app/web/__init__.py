from flask import Blueprint
from flask import render_template

web=Blueprint('web',__name__)

@web.app_errorhandler(404)
def not_found(e):               #监控所有404异常
    return render_template('404.html'),404

from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
