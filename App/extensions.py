from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager #处理用户状态保持的模块
from flask_moment import Moment
from flask_uploads import IMAGES,UploadSet,configure_uploads,patch_request_class
from flask_cache import Cache #导入缓存模块

bootstrap = Bootstrap()
db = SQLAlchemy() #ORM模型实例化
migrate = Migrate(db=db)#模型迁移
mail = Mail() #实例化邮件对象
login_manager = LoginManager()
moment = Moment()
file = UploadSet('photos',IMAGES)

#缓存模块实例化
# cache = Cache(config={'CACHE_TYPE':'simple'}) #一个简单的缓存 缓存在内存中
cache = Cache(config={'CACHE_TYPE':'redis'}) #一个简单的缓存 缓存在内存中

#初始化所有第三方扩展库
def init_app(app):
    db.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app=app)
    mail.init_app(app)
    moment.init_app(app)
    cache.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'huser.login' #指定用户登录的端点
    login_manager.login_message = '请您登录后在访问' #提示信息
    login_manager.session_protection = 'strong' #设置sessino保护级别 最强的 有任何异常 都会自动退出登录
    #文件上传配置
    configure_uploads(app,file)
    patch_request_class(app,size=None)