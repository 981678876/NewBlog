"""__author__ = 蒲金彪"""

from flask import Blueprint, render_template, request, session

from back.models import Article, Article_type, db, a_u

web_blue = Blueprint('web', __name__)


@web_blue.route('/index/', methods=['POST', 'GET'])
# 博客登录成功后的主页面
def index():
    # 提取所有的文章分类
    types = Article_type.query.all()
    if request.method == 'GET':
        # 获取当前的页数
        page = int(request.args.get('page', 1))
        # 设置每页显示的文章数量
        per_page = int(request.args.get('per_page', 3))
        # 获取当前页要显示的文章
        paginate = Article.query.order_by(Article.id).paginate(page, per_page, error_out=False)
        arts = paginate.items
        return render_template('web/list.html', types=types, arts=arts, paginate=paginate)
    if request.method == 'POST':
        # 获取需要搜索的关键字信息
        name = request.form.get('keyboard')
        # 获取包含关键字信息的所有文章
        arts = Article.query.filter(Article.title.contains(name)).all()
        return render_template('web/art_search.html', types=types, arts=arts)


@web_blue.route('/info/<int:id>/', methods=['POST', 'GET'])
def info(id):
    types = Article_type.query.all()
    if request.method == 'GET':
        # 获取文章id对应的文章
        article = Article.query.get(id)
        # 获取所有的文章
        articles = Article.query.all()
        # 获取所有文章的id
        id_nums = [art.id for art in articles]
        # 声明一个全局变量：前一篇
        prev_id = 0
        # 声明一个全局变量：后一篇
        next_id = 0
        # 判断当前文章是第一篇时
        if id == id_nums[0]:
            prev_id = id_nums[0]
            next_id = id_nums[1]
        # 判断当前文章是最后一篇时
        elif id == id_nums[-1]:
            prev_id = id_nums[-2]
            next_id = id_nums[-1]
        # 判断当前文章是中间文章时
        elif 0 < id_nums.index(id) < len(id_nums)-1:
            prev_id = id_nums[id_nums.index(id)-1]
            next_id = id_nums[id_nums.index(id)+1]
        # 判断文章数量只有一篇的情况
        elif id == id_nums[0] and id == id_nums[-1]:
            prev_id = id_nums[0]
            next_id = id_nums[-1]
        # 通过id获取前一篇文章
        prev_art = Article.query.get(prev_id)
        # 通过id获取后一篇文章
        next_art = Article.query.get(next_id)
        return render_template('web/info.html', article=article, types=types, prev_art=prev_art, next_art=next_art)
    if request.method == 'POST':
        name = request.form.get('keyboard')
        arts = Article.query.filter(Article.title.contains(name)).all()
        return render_template('web/art_search.html', types=types, arts=arts)


@web_blue.route('/note/', methods=['POST', 'GET'])
def note():
    types = Article_type.query.all()
    if request.method == 'GET':
        arts = Article.query.all()
        return render_template('web/index.html', arts=arts, types=types)
    if request.method == 'POST':
        name = request.form.get('keyboard')
        arts = Article.query.filter(Article.title.contains(name)).all()
        return render_template('web/art_search.html', types=types, arts=arts)


@web_blue.route('/about/', methods=['POST', 'GET'])
def about():
    types = Article_type.query.all()
    if request.method == 'GET':
        return render_template('web/about.html', types=types)
    if request.method == 'POST':
        name = request.form.get('keyboard')
        arts = Article.query.filter(Article.title.contains(name)).all()
        return render_template('web/art_search.html', types=types, arts=arts)


@web_blue.route('/art_category/<int:id>', methods=['POST', 'GET'])
def art_category(id):
    types = Article_type.query.all()
    if request.method == 'GET':
        arts = Article.query.filter(Article.type == id).all()
        return render_template('web/art_category.html', arts=arts, types=types)
    if request.method == 'POST':
        name = request.form.get('keyboard')
        arts = Article.query.filter(Article.title.contains(name)).all()
        return render_template('web/art_search.html', types=types, arts=arts)


@web_blue.route('/art_search/', methods=['POST', 'GET'])
def art_search():
    types = Article_type.query.all()
    if request.method == 'GET':
        return render_template('web/art_search.html', types=types)
    if request.method == 'POST':
        name = request.form.get('keyboard')
        arts = Article.query.filter(Article.title.contains(name)).all()
        return render_template('web/art_search.html', types=types, arts=arts)


@web_blue.route('/prefect_num/<int:id>', methods=['POST', 'GET'])
def prefect_num(id):
    types = Article_type.query.all()
    if request.method == 'GET':
        article = Article.query.get(id)
        articles = Article.query.all()
        id_nums = [art.id for art in articles]
        prev_id = 0
        next_id = 0
        if id == id_nums[0]:
            prev_id = id_nums[0]
            next_id = id_nums[1]
        elif id == id_nums[-1]:
            prev_id = id_nums[-2]
            next_id = id_nums[-1]
        elif 0 < id_nums.index(id) < len(id_nums) - 1:
            prev_id = id_nums[id_nums.index(id) - 1]
            next_id = id_nums[id_nums.index(id) + 1]
        elif id == id_nums[0] and id == id_nums[-1]:
            prev_id = id_nums[0]
            next_id = id_nums[-1]
        prev_art = Article.query.get(prev_id)
        next_art = Article.query.get(next_id)
        max_num = article.max_num
        max_num += 1
        article.max_num = max_num
        db.session.add(article)
        db.session.commit()
        return render_template('web/info.html', types=types, article=article, prev_art=prev_art, next_art=next_art)
    if request.method == 'POST':
        name = request.form.get('keyboard')
        arts = Article.query.filter(Article.title.contains(name)).all()
        return render_template('web/art_search.html', types=types, arts=arts)





