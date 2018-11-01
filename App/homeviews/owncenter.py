from flask import Blueprint,render_template,flash,redirect,url_for,request,current_app,jsonify
from App.models import Posts,User
from App.forms import SendPosts,Upload,UpdateInfo #导入发表博客表单类
from flask_login import current_user,login_required
from datetime import datetime
import os,string,random
from PIL import Image
from App.extensions import file
from App.extensions import db
from App.extensions import moment
#个人中心
owncenter = Blueprint('owncenter',__name__)


#修改个人信息
@owncenter.route('/update_info/',methods=['GET','POST'])
def update_info():
    form = UpdateInfo()
    if form.validate_on_submit():
        current_user.age = form.age.data
        current_user.sex = eval(form.sex.data)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('owncenter.update_info'))
    form.username.data = current_user.username
    form.age.data = current_user.age
    form.sex.data = str(int(current_user.sex))
    form.lastLogin.data = current_user.lastLogin
    form.register.data = current_user.registerTime
    return render_template('home/owncenter/update_info.html',form=form)
#time 的格式化

#博客管理
@owncenter.route('/posts_manage/')
@login_required
def posts_manage():
    posts = current_user.posts.filter_by(pid=0,state=0) #查询当前用户发表的所有帖子
    return render_template('home/owncenter/posts_manage.html',data=posts)


#修改博客的视图函数
@owncenter.route('/edit_posts/<int:pid>/',methods=['GET','POST'])
@login_required
def edit_posts(pid):
    form = SendPosts()
    p = Posts.query.get(pid)

    if form.validate_on_submit():
        p.title = form.title.data
        p.article = form.article.data
        p.timestamp=datetime.utcnow()
        p.save()
        flash('更新成功')
        return redirect(url_for('owncenter.edit_posts',pid=pid))
    # 给表单添加默认值
    form.title.data = p.title
    form.article.data = p.article
    return render_template('home/owncenter/edit_posts.html',form=form)


#删除博客
@owncenter.route('/delete_posts/<int:pid>/')
def delete_posts(pid):
    p = Posts.query.get(pid)
    p.state = 1
    p.save()
    flash('删除成功！')
    return redirect(url_for('owncenter.posts_manage'))


#上传头像

#生成随机的图片名称
def random_name(shuffix,length=64):
    #生成a-Z0-9
    Str = string.ascii_letters+string.digits
    return ''.join(random.choice(Str) for i in range(length))+'.'+shuffix

#缩放图片
def img_zoom(path,prefix,width=200,height=200):
    # 执行图片缩放
    img = Image.open(path)
    img.thumbnail((width, height))  # 缩放为100×100的图片
    pathTup = os.path.split(path)
    path = os.path.join(pathTup[0],prefix+pathTup[1])
    img.save(path)  # 保存

@owncenter.route('/upload/',methods=['GET','POST'])
def upload():
    form = Upload() #实例化表单类
    if form.validate_on_submit():
        icon = request.files.get('icon')
        suffix = icon.filename.split('.')[-1] #获取后缀
        #循环拿到唯一的图片名称
        while True:
            imgName = random_name(suffix)
            path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],imgName)
            if not os.path.exists(path):
                break
        file.save(icon,name=imgName) #保存文件 名字为新名字
        #删除之前上传的图片
        if current_user.icon != 'default.jpeg':
            delPath = current_app.config['UPLOADED_PHOTOS_DEST']+'/'
            os.remove(delPath+current_user.icon)
            os.remove(delPath+'s_'+current_user.icon)
            os.remove(delPath+'m_'+current_user.icon)
        current_user.icon = imgName
        db.session.add(current_user)
        db.session.commit()
        img_zoom(path,'m_') #执行缩放
        img_zoom(path,'s_',100,100) #执行缩放
    img_url = file.url('m_'+current_user.icon) #通过图片名称 拿到url地址
    return render_template('home/owncenter/upload_photos.html',form=form,img_url=img_url)


#我的收藏
@owncenter.route('/my_favorite/')
@login_required
def my_favorite():
    data = current_user.favorites.all() #拿到所有当前用户收藏的博客
    return render_template('home/owncenter/my_favorite.html',data=data)

