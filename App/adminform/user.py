from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,RadioField,HiddenField
from wtforms.validators import DataRequired,Length,Email,ValidationError,EqualTo
from App.models import User

#后台添加用户
class AdminUser(FlaskForm):
    uid = HiddenField()
    username = StringField('用户名',validators=[DataRequired('用户名不能为空'),Length(min=6,max=12,message='用户名在6～12位之间')],render_kw={'minlength':6,'maxlength':12,'placeholder':'请输入用户名'})
    userpass = PasswordField('密码',render_kw={'minlength':6,'maxlength':12,'placeholder':'请输入密码'})
    passwordconfirm = PasswordField('确认密码',validators=[EqualTo('userpass',message='密码和确认密码不一致')],render_kw={'minlength':6,'maxlength':12,'placeholder':'请输入确认密码'})
    email = StringField('邮箱',validators=[DataRequired(message='邮箱不能为空'),Email(message='请输入正确的邮箱地址')],render_kw={'maxlength':100,'placeholder':'请输入邮箱'})
    # 自定义表单验证器
    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('该用户已存在 请重新输入')
    #
    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('该邮箱已存在 请重新输入')

            # 自定义表单验证器

    def validate_username(self, field):
        newU = User.query.filter_by(username=field.data).first()
        hidden = self.uid.data
        if hidden:
            uid = eval(hidden)
            newU = User.query.filter_by(username=field.data).first()
            if newU:
                if newU.id != uid:
                    raise ValidationError('该用户已存在 请重新输入')
        else:
            if newU:
                raise ValidationError('该用户已存在 请重新输入')

    def validate_email(self, field):
        hidden = self.uid.data
        newU = User.query.filter_by(email=field.data).first()
        if hidden:
            uid = eval(hidden)
            if newU:
                if newU.id != uid:
                    raise ValidationError('邮箱已存在 请重新输入')
        else:
            if newU:
                raise ValidationError('该邮箱已存在 请重新输入')
"""
DataRequired(message='密码不能为空'),Length(min=6,max=12,message='密码在6～12位之间')]
DataRequired(message='确认密码不能为空'),Length(min=6,max=12,message='密码在6～12位之间'),
"""
"""
#后台添加用户
class AdminEditUser(FlaskForm):
    uid = HiddenField()
    username = StringField('用户名',validators=[DataRequired('用户名不能为空'),Length(min=6,max=12,message='用户名在6～12位之间')],render_kw={'minlength':6,'maxlength':12,'placeholder':'请输入用户名'})
    userpass = PasswordField('密码',render_kw={'minlength':6,'maxlength':12,'placeholder':'请输入密码'})
    passwordconfirm = PasswordField('确认密码',validators=[EqualTo('userpass',message='密码和确认密码不一致')],render_kw={'minlength':6,'maxlength':12,'placeholder':'请输入确认密码'})
    email = StringField('邮箱',validators=[DataRequired(message='邮箱不能为空'),Email(message='请输入正确的邮箱地址')],render_kw={'maxlength':100,'placeholder':'请输入邮箱'})
    # 自定义表单验证器
    def validate_username(self, field):
        uid = eval(self.uid.data)
        # u = User.query.get(uid)
        newU = User.query.filter_by(username=field.data).first()
        if newU:
            if newU.id != uid:
                raise ValidationError('该用户已存在 请重新输入')

    def validate_email(self, field):
        uid = eval(self.uid.data)
        newU = User.query.filter_by(email=field.data).first()
        if newU:
            if newU.id != uid:
                raise ValidationError('邮箱已存在 请重新输入')
"""