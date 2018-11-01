from flask import Blueprint,render_template,request,current_app,redirect,url_for
from App.models import Posts
from App.extensions import cache #导入缓存对象
hmain = Blueprint('hmain',__name__)
"""
@hmain.route('/')
# @cache.cached(timeout=60) #缓存时间1分钟
def index():
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1
    return redirect(url_for('hmain.mainShow',page=page))

@hmain.route('/index/<int:page>/')
@cache.memoize(timeout=60) #缓存时间1分钟
def mainShow(page):
    print('-------------看看我走几次-------------')
    pagination = Posts.query.filter_by(pid=0).order_by(Posts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
    data = pagination.items  # 获取page页面的数据
    return render_template('home/main/index.html', data=data, pagination=pagination)

"""

@hmain.route('/clear_cache/')
def clear_cache():
    cache.clear()
    return '清除所有缓存'

@hmain.route('/')
def index():
    try:
        page = int(request.args.get('page',1))
    except:
        page = 1
    key = 'page'+str(page)
    data = cache.get(key)
    if not data:
        print('没走缓存')
        pagination = Posts.query.filter_by(pid=0).order_by(Posts.timestamp.desc()).paginate(page, current_app.config[
            'PAGE_NUM'], False)
        data = render_template('home/main/index.html', data=pagination.items, pagination=pagination)
        cache.set(key, data, timeout=60)
    return data


#手动设置缓存
@hmain.route('/test_cache/')
def test_cache():
    page = request.args.get('page','1')
    key = 'page'+page
    data = cache.get(key)
    if not data:
        print('没走缓存')
        # newVal =
        data = '我是第'+page+'页的数据'
        cache.set(key,data,timeout=60)

    return data


"""
@hmain.route('/')
def index():
    try:
        page = int(request.args.get('page',1))
    except:
        page = 1
    pagination = Posts.query.filter_by(pid=0).order_by(Posts.timestamp.desc()).paginate(page,current_app.config['PAGE_NUM'],False)
    data = pagination.items #获取page页面的数据
    return render_template('home/main/index.html',data=data,pagination=pagination)
"""