from flask import Blueprint,render_template

#后台首页
amain = Blueprint('amain',__name__)
@amain.route('/')
def index():
    return render_template('admin/main/index.html')
