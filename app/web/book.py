import json

from flask import jsonify,request

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel,BookCollection
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
    books=BookCollection()

    if form.validate():                                         #SearchForm验证通过会返回True,否则返回False
        q=form.q.data.strip()
        page=form.page.data
        isbn_or_key=is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key=='isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q,page)

        books.fill(yushu_book,q)
        return json.dumps(books,default=lambda o:o.__dict__,ensure_ascii=False)    #递归books下的每一个实例属性，都将其转化为dict形式
        # return jsonify(books.__dict__)                        #(这样不可以，因为BookCollection的books属性还是对象形式存在。)将实例属性转化为字典
    else:
        return jsonify(form.errors)                             #WTForms验证不通过会将错误信息放在errors属性中