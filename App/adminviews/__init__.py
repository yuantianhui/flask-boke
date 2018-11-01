from .main import amain as adminMain
from .user import auser as adminUser
blueprint_config = [
    (adminMain,'/admin'), #个人中心 博客管理
    (adminUser,'/user'), #个人中心 博客管理
]



#注册蓝本
def admin_register_blueprint(app):
    for blueprint,prefix in blueprint_config:
        app.register_blueprint(blueprint,url_prefix=prefix)