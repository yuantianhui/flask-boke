from flask import Flask,render_template,flash,request,session,abort
from .settings import configDict #导入配置的字典
from .extensions import init_app #初始化第三方扩展库
from .homeviews import home_register_blueprint #注册蓝本
from .adminviews import admin_register_blueprint
from App.models import Posts


def create_app(configMame):
    app = Flask(__name__)
    app.config.from_object(configDict[configMame]) #加载配置类
    init_app(app)
    home_register_blueprint(app) #前台的蓝本的注册
    admin_register_blueprint(app) #后台蓝本的注册
    do_error(app)
    middleware(app)
    addTemFilter(app)
    return app


#错误处理
def do_error(app):
    @app.errorhandler(404)
    def page_not_found(err):
        flash('您访问的页面不存在')
        return render_template('error.html',title='404 page not found')

    @app.errorhandler(500)
    def server_error(err):
        flash('您访问的太热情了 请稍候再次访问～')
        return render_template('error.html',title='500 server error')


#钩子函数 类似就是django的中间件  在请求和响应之间进行过滤
def middleware(app):
    @app.before_first_request
    def before_first_request():
        pass
    @app.before_request
    def before_request():
        # print(request.path)
        if request.path == '/admin/' and not session.get('aid'):
            abort(500) #跳到后台登录界面

    @app.after_request
    def after_request(res):
        return res

    @app.teardown_request
    def teardown_request(res):
        return res


def addTemFilter(app):
    #自定义模板过滤器
    #计算字符串中逗号的个数
    def countd(Str):
        return Str.count(',')

    def replayName(pid):
        username = Posts.query.get(int(pid)).user.username
        return username


    # 可以给过滤器器一个名字，如果没有，默认就是函数的名字
    app.add_template_filter(countd)
    app.add_template_filter(replayName)





