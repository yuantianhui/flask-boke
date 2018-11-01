from App.extensions import db
from datetime import datetime
from .publiclass import Base


#帖子模型
class Posts(Base,db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(20),index=True)
    article = db.Column(db.Text)
    pid = db.Column(db.Integer,default=0)
    path = db.Column(db.Text,default='0,')
    visit = db.Column(db.Integer,default=0) #访问量
    fabulous = db.Column(db.Integer,default=0) #点赞量
    timestamp = db.Column(db.DateTime,default=datetime.utcnow) #发表的时间
    #设置一对多外键
    uid = db.Column(db.Integer,db.ForeignKey('user.id')) #设置外键 关联user表的子增id
    state = db.Column(db.Integer,default=0) #当用户选择删除的时候 只更改状态 在后台依然可以查询到
