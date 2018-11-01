from flask import Blueprint,render_template,flash,redirect,url_for,request,current_app,jsonify
from App.models import User,Posts
from App.forms import SendPosts
from flask_login import current_user
from sqlalchemy import or_
from App.extensions import db


hposts = Blueprint('hposts',__name__)

#首页展示
@hposts.route('/send_posts/',methods=['GET','POST'])
def send_posts():
    form = SendPosts()
    #判断是否登录
    if not current_user.is_authenticated:
        flash('您还没有登录 请登录后在发表')
    else:
        if form.validate_on_submit():
            p = Posts(title=form.title.data,article=form.article.data,user=current_user)
            p.save()
            flash('发表成功！')
            return redirect(url_for('hposts.send_posts'))
    return render_template('home/posts/send_posts.html', form=form)

#博客详情
@hposts.route('/posts_detail/<int:pid>/')
def posts_detail(pid):
    #查询当前帖子的数据
    posts = Posts.query.get(pid)
    form = SendPosts()
    comment = Posts.query.filter(Posts.path.contains(str(pid)),Posts.state==0).order_by(Posts.path.concat(Posts.id))
    return render_template('home/posts/posts_detail.html',posts=posts,form=form,pid=pid,comment=comment)










@hposts.route('/comment/',methods=['POST'])
def comment():
    print(request.form)
    rid = request.form.get('rid')
    pid = request.form.get('pid')

    if rid:
        id = rid
    else:
        id = pid
    p = Posts.query.get(int(id))
    Posts(article=request.form.get('article'),pid=id,path=p.path+id+',',user=current_user).save()
    return redirect(url_for('hposts.posts_detail',pid=pid))


#搜索
@hposts.route('/search/',methods=['GET','POST'])
def search():
    try:
        page = int(request.args.get('page',1))
    except:
        page = 1

    if request.method == 'GET':
        word = request.args.get('con','')
    else:
        word = request.form.get('con','')

    pagination = Posts.query.filter(or_(Posts.title.contains(word),Posts.article.contains(word))).paginate(page,current_app.config['PAGE_NUM'],False)
    data = pagination.items
    return render_template('home/posts/search.html',data=data,word=word,pagination=pagination)

#收藏操作
@hposts.route('/do_favorite/')
def do_favorite():
    try:
        pid = int(request.args.get('pid'))
        # print(pid)
        if current_user.is_favorite(pid):
            #取消收藏
            current_user.delete_favorite(pid)
            print('delete_favorite')
        else:
            #添加收藏
            current_user.add_favorite(pid)
            print('add_favorite')
        return jsonify({'res': 200})
    except:
        return jsonify({'res':500})