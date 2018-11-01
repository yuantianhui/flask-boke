from flask import Blueprint,render_template,redirect,url_for,flash
from App.forms import Register,AgainActivate,Login #导入表单类
from App.models import User #导入用户模型类
from App.email import send_mail #导入发送邮件
from flask_login import login_required,login_user,logout_user,current_user
from datetime import datetime
from App.extensions import cache

#huser == homeuser前台的用户蓝本的访问

huser = Blueprint('huser',__name__)



#注册
@huser.route('/register/',methods=['GET','POST'])
def register():
    cache.clear()
    form = Register()
    if form.validate_on_submit():
        u = User(username=form.username.data,password=form.userpass.data,email=form.email.data)
        u.save()
        # #生成token
        token = u.generate_token()
        #发送邮件
        send_mail('邮件激活',u.email,endpoint='huser.activate',username=u.username,token=token)
        flash('注册成功 请前往邮箱进行最后一步的激活操作！')
        return redirect(url_for('huser.login')) #跳转到登录
    return render_template('home/user/register.html',form=form)

#账户激活
@huser.route('/activate/<token>/')
def activate(token):
    cache.clear()
    if User.check_token(token):
        flash("激活成功")
        return redirect(url_for('huser.login')) #跳转到登录
    flash('激活失败 请重新进行账户激活')
    return redirect(url_for('huser.register')) #跳转到登录


#再次激活视图函数
@huser.route('/again_activate/',methods=['GET','POST'])
def again_activate():
    form = AgainActivate()
    cache.clear()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        if not u.check_password(form.userpass.data):
            flash('请输入正确密码')
        elif not u.confirm:
            token = u.generate_token()
            # 发送邮件
            send_mail('邮件激活', u.email, endpoint='huser.activate', username=u.username, token=token)
            flash('激活邮件发送成功 请前往邮箱进行激活操作！')

        else:
            flash('该账户已经激活 请前去登录！')
    return render_template('home/user/again_activate.html',form=form)



#登录
@huser.route('/login/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        cache.clear()
        if not u:
            flash('该用户不存在')
        elif not u.confirm:
            flash('该用户未激活 请前去激活')
        elif not u.check_password(form.userpass.data):
            flash('请输入正确的密码')
        else:
            flash('登录成功!')
            u.lastLogin = datetime.utcnow()
            u.save()
            login_user(u,remember=form.remember.data)
            return redirect(url_for('hmain.index'))

    return render_template('home/user/login.html',form=form)

#退出登录
@huser.route('/logout/')
def logout():
    logout_user()
    flash('退出成功！')
    cache.clear()
    return redirect(url_for('hmain.index'))


@huser.route('/test/')
@login_required
def test():
    return '必须登录才能访问'