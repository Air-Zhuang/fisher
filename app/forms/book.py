from wtforms import Form,StringField,IntegerField
from wtforms.validators import Length,NumberRange,DataRequired

class SearchForm(Form):
    '''default:默认值,message:自定义错误提示,DataRequired:内容不能为空'''
    q=StringField(validators=[DataRequired(),Length(min=1,max=30)])
    page=IntegerField(validators=[NumberRange(min=1,max=99)],default=1)