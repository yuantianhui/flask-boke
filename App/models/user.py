from App.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash#密码生成验证模块
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize #序列化模块
from flask import current_app
from flask_login import UserMixin #判断是否登录等方法的类
from App.extensions import login_manager
from .publiclass import Base
from .posts import Posts


#user模型类
class User(UserMixin,Base,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(12),index=True)
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.Boolean,default=True)
    age = db.Column(db.Integer,default=18)
    email = db.Column(db.String(100))
    icon = db.Column(db.String(70),default='default.jpeg')
    role = db.Column(db.Boolean,default=False) #用户角色 普通用户还是管理员 默认为普通用户
    lastLogin = db.Column(db.DateTime)
    registerTime = db.Column(db.DateTime,default=datetime.utcnow) #注册时间（默认的）
    confirm = db.Column(db.Boolean,default=False) #激活状态
    #设置密码属性不可读

    #设置引用关系
    """
    Posts 建立引用关系的模型
    backref 是给关联的模型添加一个属性 叫user
    lazy 加载的时机  返回查询集（你可以在拼接过滤器）如果不给lazy 默认则为select模式（一旦调用posts 则就返回数据 不能在拼接过滤器 也就是你的链式调用）
    作用
    u.posts.all() 拿到所有的帖子
    p.user 获取到当前帖子的用户
    """
    posts = db.relationship('Posts',backref='user',lazy='dynamic')
    #在flask多对多里 要指定查询数据的中间表 secondary
    """
    u.favorites.all() 查询当前用户收藏了哪些帖子
    p.users.all()  查询帖子都被谁收藏了
    """
    favorites = db.relationship('Posts',secondary='collections',backref=db.backref('users',lazy='dynamic'),lazy='dynamic')

    @property
    def password(self):
        raise AttributeError
    #生成加密
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    #验证密码
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    #生成token
    def generate_token(self):
        s = Seralize(current_app.config['SECRET_KEY'])
        return s.dumps({'id':self.id}) #返回一个字符串

    #检测token 进行激活
    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        try:
            Dict = s.loads(token)
            id = Dict['id']
            u = User.query.get(id)
            if not u:
                return False
            u.confirm = True
            u.save()
            return True
        except:
            return False

    #判断是否收藏博客的方法
    def is_favorite(self,pid):
        p = self.favorites.all()
        for row in p:
            if row.id==pid:
                return True
        return False
        # return len(list(filter(lambda p:p.id==pid,p)))
        # 添加收藏
    def add_favorite(self, pid):
        self.favorites.append(Posts.query.get(int(pid)))
        db.session.commit()

    #取消收藏
    def delete_favorite(self,pid):
        self.favorites.remove(Posts.query.get(int(pid)))
        db.session.commit()




#这是一个回调方法 实时获取表中当前用户数据的对象
@login_manager.user_loader
def user_loader(userid):
    return User.query.get(int(userid))


