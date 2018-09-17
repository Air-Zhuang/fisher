from app import mail
from flask_mail import Message

#to,subject,template
def send_mail():
    msg=Message('测试邮件',sender='1993742965@qq.com',body='Test',recipients=['1993742965@qq.com'])
    mail.send(msg)
