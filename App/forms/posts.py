from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length

class SendPosts(FlaskForm):
    title = StringField('标题',validators=[DataRequired(message='标题不能为空'),Length(min=6,max=20,message='标题内容在6~20字之间')],render_kw={'placeholder':'请输入标题'})
    article = TextAreaField('内容',validators=[DataRequired(message='博客内容不能为空'),Length(min=10,max=5000,message='博客内容在10～5000字之间')],render_kw={'placeholder':'请输入博客内容...','style':'resize:none;height:300px;'})
    submit = SubmitField('发表')