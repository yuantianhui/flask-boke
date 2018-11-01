from .user import huser as homeuser
from .main import hmain as homemain
from .posts import hposts as homeposts
from .owncenter import owncenter as homeowncenter

blueprint_config = [
    (homeuser,''),#用户的登录注册 再次激活
    (homemain,''), #首页的展示
    (homeposts,''), #帖子的发表 详情 搜索
    (homeowncenter,''), #个人中心 博客管理
]



#注册蓝本
def home_register_blueprint(app):
    for blueprint,prefix in blueprint_config:
        app.register_blueprint(blueprint,url_prefix=prefix)