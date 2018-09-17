from . import web

from app.models.base import db
from flask import render_template,request,redirect,url_for,flash
from app.forms.auth import RegisterForm,LoginForm,EmailForm
from app.models.user import User
from flask_login import login_user, logout_user


@web.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        with db.auto_commit():
            user=User()
            user.set_attrs(form.data)               #传入数据以字典形式
            db.session.add(user)
        # db.session.commit()
        return redirect(url_for('web.login'))
    return render_template('auth/register.html',form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm(request.form)
    if request.method=='POST' and form.validate():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 五步：1、init文件初始化flask_login 2、model层绑定属性和装饰器 3、这里写cookie 4、在需要验证登录的控制器上加@login_required装饰器 5、从current_user中提取用户信息
            login_user(user,remember=True)              # 将这个字段写入到cookie
            next=request.args.get('next')               #这四行实现了如果cookie失效被flask_login重定向到主页之后再登录能够返回到重定向之前的页面
            print(next)
            if not next or not next.startswith('/'):    #or not next.startswith('/')实现的防止重定向攻击的功能
                next=url_for('web.index')
            return redirect(next)
        else:
            flash("账号不存在或密码错误")

    return render_template('auth/login.html',form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method=='POST':
        if form.validate():             #真正让消息闪现的是这句话form.validate()
            account_email=form.email.data
            user=User.query.filter_by(email=account_email).first_or_404()   #从数据库查询用户消息。返回第一个结果，如果没有抛出404异常，跳到404页面
    return render_template('auth/forget_password_request.html',form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
