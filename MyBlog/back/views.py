"""__author__ = 蒲金彪"""

from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from back.models import User, Article, Article_type, db
from utils.functions import is_login

back_blue = Blueprint('back', __name__)


@back_blue.route('/index/', methods=['POST', 'GET'])
# 校验用户信息
@is_login
def index():
    # 校验成功后返回页面
    return render_template('back/index.html')


@back_blue.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        # 获取提交的用户名、密码
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 判断信息是否输入完整
        if username and password and password2:
            # 获取数据库中的用户信息
            user = User.query.filter(User.username == username).first()
            # 判断用户是否存在
            if user:
                error = '该账号已被注册，请更换新账号'
                return render_template('back.register.html', error=error)
            # 不存在就创建
            else:
                # 判断两次密码输入是否一致
                if password == password2:
                    # 创建一个用户对象
                    user = User()
                    # 添加用户名
                    user.username = username
                    # 通过generate_password_hash加密
                    user.password = generate_password_hash(password)
                    # 调用save方法将用户对象保存到数据库中
                    user.save()
                    return redirect(url_for('back.login'))
                # 两次密码不一致做的事情
                else:
                    error = '两次输入密码不一致'
                    return render_template('back/register.html', error=error)
        # 信息输入不完整做的事情
        else:
            error = '信息请填写完整'
            return render_template('back/register.html', error=error)


@back_blue.route('/login/', methods=['POST', 'GET'])
# 注册成功后跳转到此登录页面
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        # 获取提交的用户信息
        username = request.form.get('username')
        password = request.form.get('password')
        # 判断用户信息是否填写完整
        if username and password:
            user = User.query.filter(User.username == username).first()
            # 判断用户是否注册过
            if user:
                # 判断密码是否正确
                if check_password_hash(user.password, password):
                    # 添加session信息
                    session['user_id'] = user.id
                    return redirect(url_for('back.index'))
                else:
                    error = '密码输入错误'
                    return render_template('back/login.html', error=error)
            else:
                error = '账号输入错误'
                return render_template('back/login.html', error=error)

        else:
            error = '信息请填写完整'
            return render_template('back/login.html', error=error)


@back_blue.route('/logout/')
def logout():
    # 删除session信息
    del session['user_id']
    return redirect(url_for('back.login'))


@back_blue.route('/a_type/', methods=['POST', 'GET'])
def a_type():
    if request.method == 'GET':
        # 获取所有的文章分类
        types = Article_type.query.all()
        return render_template('back/category_list.html', types=types)


@back_blue.route('/add_type/', methods=['POST', 'GET'])
# 添加文章分类
def add_type():
    if request.method == 'GET':
        return render_template('back/category_detail.html')
    if request.method == 'POST':
        # 获取提交的文章分类名
        atype = request.form.get('atype')
        # 判断是否输入信息
        if atype:
            # 创建文章分类对象
            art_type = Article_type()
            # 给对象添加分类名
            art_type.t_name = atype
            # 调用save方法后提交至数据库
            art_type.save()
            return redirect(url_for('back.a_type'))
        else:
            error = '请填写文章分类名称'
            return render_template('back/category_detail.html', error=error)


@back_blue.route('/del_type/<int:id>/', methods=['GET', 'POST'])
# 删除文章分类
def del_type(id):
    if request.method == 'GET':
        # 获取要删除的文章分类数据
        dele_type = Article_type.query.get(id)
        # 删除
        db.session.delete(dele_type)
        # 提交更新数据库
        db.session.commit()
        return redirect(url_for('back.a_type'))


@back_blue.route('/article_list/', methods=['GET', 'POST'])
# 文章列表
def article_list():
    if request.method == 'GET':
        # arts = Article.query.all()
        # 查询第几页的数据
        page = int(request.args.get('page', 1))
        # 每一页的条数是多少，默认为10条
        per_page = int(request.args.get('per_page', 3))
        # 查询当前第几个的多少条数据
        paginate = Article.query.order_by(Article.id).paginate(page, per_page, error_out=False)
        # 获取所有的文章
        arts = paginate.items
        return render_template('back/article_list.html', arts=arts, paginate=paginate)


@back_blue.route('/article_add/', methods=['POST', 'GET'])
# 添加文章
def article_add():
    if request.method == 'GET':
        types = Article_type.query.all()
        return render_template('back/article_detail.html', types=types)
    if request.method == 'POST':
        # 获取文章的标题
        title = request.form.get('name')
        # 获取文章的描述
        desc = request.form.get('desc')
        # 获取文章的分类
        category = request.form.get('category')
        # 获取文章的内容
        content = request.form.get('content')
        # 判断信息是否输入完整
        if title and desc and category and content:
            # 添加信息，并将信息提交给数据库
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            art.type = category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article_list'))
        else:
            error = '请填写完整的文章信息'
            return render_template('back/article_detail.html', error=error)


@back_blue.route('/article_editor/<int:id>/', methods=['GET', 'POST'])
# 修改文章信息
def article_editor(id):
    if request.method == 'GET':
        types = Article_type.query.all()
        return render_template('back/article_detail.html', types=types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        art_editor = Article.query.get(id)
        art_editor.title = title
        art_editor.desc = desc
        art_editor.content = content
        art_editor.type = category
        db.session.add(art_editor)
        db.session.commit()
        return redirect(url_for('back.article_list'))


@back_blue.route('/article_del/<int:id>/', methods=['POST', 'GET'])
# 删除文章
def article_del(id):
    if request.method == 'GET':
        del_article = Article.query.get(id)
        db.session.delete(del_article)
        db.session.commit()
        return redirect(url_for('back.article_list'))


@back_blue.route('/article_page/', methods=['POST', 'GET'])
# 给文章添加分页功能
def article_page():
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 3))
        paginate = Article.query.order_by(Article.id).paginate(page, per_page, error_out=False)
        arts = paginate.items
        # page = id
        # arts = Article.query.offset((page-1)*3).limit(3).all()
        return render_template('back/article_list.html', arts=arts, paginate=paginate)


@back_blue.route('/user_message/', methods=['POST', 'GET'])
# 显示所有用户信息
def user_message():
    if request.method == 'GET':
        users = User.query.all()
        return render_template('back/user_list.html', users=users)


@back_blue.route('/user_editor/<int:id>/', methods=['POST', 'GET'])
# 修改用户密码
def user_editor(id):
    if request.method == 'GET':
        return render_template('back/user_detail.html')
    if request.method == 'POST':
        # 获取用户的密码
        password = request.form.get('password')
        user = User.query.get(id)
        user.password = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('back.user_message'))


@back_blue.route('/user_del/<int:id>/', methods=['POST', 'GET'])
# 删除用户
def user_del(id):
    if request.method == 'GET':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('back.user_message'))



















