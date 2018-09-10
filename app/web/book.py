from flask import jsonify,request

from app.forms.book import SearchForm
from helper import is_isbn_or_key
from yushu_book import YuShuBook
from . import web


@web.route('/book/search')
def hello():
    '''
        doubanapi:
            http://t.yushu.im/v2/book/search?q={}&count={}&start={}
            http://api.douban.com/v2/book/isbn/{isbn}
        api:
            http://t.yushu.im/v2/book/search?q={}&count={}&start={}
            http://t.yushu.im/v2/book/isbn/{isbn}
        q:普通关键字/isbn
        page
        isbn:isbn13 13个0到9的数字组成            (新)
             isbn10 10个0到9数字组成，含有一些'-'  (旧)
    '''
    form=SearchForm(request.args)
    if form.validate():             #SearchForm验证通过会返回True,否则返回False
        q=form.q.data.strip()
        page=form.page.data
        isbn_or_key=is_isbn_or_key(q)
        if isbn_or_key=='isbn':
            result=YuShuBook.search_by_isbn(q)
        else:
            result=YuShuBook.search_by_keyword(q)
        return jsonify(result)
    else:
        return jsonify(form.errors)     #WTForms验证不通过会将错误信息放在errors属性中