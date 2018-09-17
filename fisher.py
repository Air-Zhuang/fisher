from flask import Flask

from app import create_app

app=create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=app.config['DEBUG'])
    '''
    http://127.0.0.1:5000/book/search/郭敬明/1
    http://t.yushu.im/v2/book/isbn/9787501524044
    http://127.0.0.1:5000/book/search/9787501524044/1
    http://127.0.0.1:5000/book/search?q=9787501524044&page=1
    http://127.0.0.1:5000/book/9787501524044/detail
    '''