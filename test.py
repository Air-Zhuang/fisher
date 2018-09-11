from flask import Flask,current_app

app=Flask(__name__)
'''
应用上下文 对象 Flask
请求上下文 对象 Request
Flask AppContext
Request RequestContext
离线应用、单元测试
'''
#写法一
ctx=app.app_context()
ctx.push()
a=current_app
d=current_app.config['DEBUG']
ctx.pop()
#写法二
with app.app_context():
    a = current_app
    d = current_app.config['DEBUG']