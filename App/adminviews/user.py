from flask import Blueprint,render_template,request,redirect,url_for
from App.adminform import AdminUser #导入添加用户的表单类
from App.models import User #导入user模型类
#admin_user 后台用户管理
auser = Blueprint('auser',__name__)

#用户管理的首页
@auser.route('/')
def index():
    u = User.query.order_by(-User.id)
    return render_template('admin/User/index.html',data=u)


#添加用户
@auser.route('/add_user/',methods=['GET','POST'])
def add_user():
    form = AdminUser()
    if form.validate_on_submit():
        u = User(username=form.username.data,password=form.userpass.data,email=form.email.data,role=eval(request.form.get('role')),confirm=eval(request.form.get('confirm')))
        u.save()
        return redirect(url_for('auser.index'))
    return render_template('admin/User/add.html',form=form)


#编辑用户
@auser.route('/edit_user/',methods=['GET','POST'])
def edit_user():
    uid = int(request.args.get('uid'))
    u = User.query.get(uid)
    form = AdminUser()
    if form.validate_on_submit():
        u = User.query.get(int(form.uid.data))
        u.username = form.username.data
        u.email = form.email.data
        u.role = int(request.form.get('role'))
        u.confirm = int(request.form.get('confirm'))
        u.save()
        return redirect(url_for('auser.index'))
    form.username.data = u.username
    form.email.data = u.email
    form.uid.data = uid
    return render_template('admin/User/edit.html',u=u,form=form)











