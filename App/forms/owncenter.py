from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField,FileRequired
from wtforms import SubmitField,StringField,IntegerField,RadioField
from wtforms.validators import NumberRange,DataRequired
from App.extensions import file

#文件上传表单类
class Upload(FlaskForm):
    icon = FileField('上传头像',validators=[FileRequired(message='您还没有选择文件'),FileAllowed(file,message='该文件类型不允许上传')])
    submit = SubmitField('上传')

#修改个人信息的表单类
class UpdateInfo(FlaskForm):
    username = StringField('用户名',render_kw={'readonly':'True'})
    age = IntegerField('年龄',validators=[DataRequired(message='年龄不能为空'),NumberRange(min=1,max=100,message='年龄在1～100岁之间')])
    sex = RadioField('性别',choices=[('1','男'),('0','女')],validators=[DataRequired(message='性别必选')])
    lastLogin = StringField('上次登录时间',render_kw={'disabled':'True'})
    register = StringField('注册时间',render_kw={'disabled':'True'})
    submit = SubmitField('修改')