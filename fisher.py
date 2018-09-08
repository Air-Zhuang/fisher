from flask import Flask,make_response
from helper import is_isbn_or_key

app=Flask(__name__)
app.config.from_object('config')

@app.route('/book/search/<q>/<page>')   #这样会识别成请求参数
def hello(q,page):
    '''
        api:http://t.yushu.im/v2/book/search?q={}&start={}&count={}
            http://t.yushu.im/v2/book/isbn/{isbn}
        q:普通关键字/isbn
        page
        isbn:isbn13 13个0到9的数字组成            (新)
             isbn10 10个0到9数字组成，含有一些'-'  (旧)
    '''
    isbn_or_key=is_isbn_or_key(q)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=app.config['DEBUG'])