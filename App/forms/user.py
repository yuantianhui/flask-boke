from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from App.models import User #导入User模型类

#注册表单类
class Register(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='用户名不能为空'),Length(min=6,max=12,message='用户名长度范围在6～12位之间')],render_kw={'placeholder':'请输入用户名...'})
    userpass = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=12,message='密码长度范围在6～12位之间')],render_kw={'placeholder':'请输入密码...'})
    confirm = PasswordField('确认密码',validators=[DataRequired(message='确认密码不能为空'),Length(min=6,max=12,message='确认密码长度范围在6～12位之间'),EqualTo('userpass',message='密码和确认密码不一致')],render_kw={'placeholder':'请输入确认密码...'})
    email = StringField('激活邮箱',validators=[DataRequired(message='用于激活的邮箱地址不能为空'),Email(message='请输入正确的邮箱地址')],render_kw={'placeholder':'请输入用于账户激活的邮箱...'})
    submit = SubmitField('注册')
    #自定义表单验证器
    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已存在 请重新输入')
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已存在 请重新输入')

#再次激活表单类
class AgainActivate(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='用户名不能为空'),Length(min=6,max=12,message='用户名长度范围在6～12位之间')],render_kw={'placeholder':'请输入用户名...'})
    userpass = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=12,message='密码长度范围在6～12位之间')],render_kw={'placeholder':'请输入密码...'})
    submit = SubmitField('激活')
    #自定义表单验证器
    def validate_username(self,field):
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户不存在 请重新输入')


#登录表单类
class Login(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='用户名不能为空'),Length(min=6,max=12,message='用户名长度范围在6～12位之间')],render_kw={'placeholder':'请输入用户名...'})
    userpass = PasswordField('密码',validators=[DataRequired(message='密码不能为空'),Length(min=6,max=12,message='密码长度范围在6～12位之间')],render_kw={'placeholder':'请输入密码...'})
    remember = BooleanField('记住用户名')
    submit = SubmitField('登录')

