import json

from flask import jsonify,request,render_template,flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel,BookCollection
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
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
        # return json.dumps(books,default=lambda o:o.__dict__,ensure_ascii=False)    #递归books下的每一个实例属性，都将其转化为dict形式
        # return jsonify(books.__dict__)                        #(这样不可以，因为BookCollection的books属性还是对象形式存在。)将实例属性转化为字典
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)

@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts=False      #当前用户是否是赠送者
    has_in_wishes=False     #当前用户是否是索求者

    #取书籍详情数据
    yushu_book=YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book=BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,isbn=isbn, launched=False).first():#如果能查到，说明当前用户是赠送者
            has_in_gifts=True
        if Wish.query.filter_by(uid=current_user.id,isbn=isbn, launched=False).first():#如果能查到，说明当前用户是索求者
            has_in_wishes=True

    trade_gifts=Gift.query.filter_by(isbn=isbn,launched=False).all()    #查询所有赠送人的清单
    trade_wishes=Wish.query.filter_by(isbn=isbn,launched=False).all()   #查询所有想要书的人的清单

    trade_wishes_model=TradeInfo(trade_wishes)          #将从数据库提取出来的数据结构变形成可供页面识别的数据结构
    trade_gifts_model=TradeInfo(trade_gifts)

    return render_template('book_detail.html',book=book,wishes=trade_wishes_model,
                           gifts=trade_gifts_model,has_in_gifts=has_in_gifts,has_in_wishes=has_in_wishes)


