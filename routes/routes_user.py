from urllib.parse import unquote_plus

from models.session import Session
from routes import (
    JinjaTemplateRender,
    current_user,
    html_response,
    random_string,
    redirect,
)

from utils import log
from models.user import User


def login(request):
    """
    登录页面的路由函数
    """
    form = request.form()

    u, result = User.login(form)
    # session 会话
    # token 令牌
    # 设置一个随机字符串来当令牌使用
    session_id = random_string()
    form = dict(
        session_id=session_id,
        user_id=u.id,
    )
    Session.new(form)

    headers = {
        'Set-Cookie': 'session_id={}; path=/'.format(
            session_id
        )
    }

    return redirect('/user/login/view?result={}'.format(result), headers)


def login_view(request):
    u = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)

    body = JinjaTemplateRender.render(
        'login.html',
        username=u.username,
        result=result,
    )
    return html_response(body)


def register(request):
    """
    注册页面的路由函数
    """
    form = request.form()

    u, result = User.register(form)
    log('register post', result)

    return redirect('/user/register/view?result={}'.format(result))


def register_view(request):
    result = request.query.get('result', '')
    result = unquote_plus(result)

    body = JinjaTemplateRender.render('register.html', result=result)
    return html_response(body)


def update_user_password(request):
    # route_admin_update
    """
    管理员修改用户信息
    """
    result = ''

    # 取到管理员输入的用户 id 和新密码
    form = request.form()

    # 重置密码加盐
    salted_pw = str(User.salted_password(form['password']))

    # 调用 User 的 update 方法，修改用户密码
    User.update(form, salted_pw)

    # 返回到管理员查看用户信息的页面
    result += 'password_modified'
    return redirect('/admin/edit_password?result={}'.format(result))


def edit_password(request):
    # route_admin_view
    """
    管理员查看用户信息
    """
    u = current_user(request)
    result = request.query.get('result', '')
    result = unquote_plus(result)
    users = User.all()

    body = JinjaTemplateRender.render(
        'admin_password_edit.html',
        users=users,
        username=u.username,
        result=result,
    )
    return html_response(body)


def admin_required(route_function):

    def f(request):
        u = current_user(request)
        if u.is_admin():
            return route_function(request)
        else:
            return redirect('/user/login/view')

    return f


def route_dict():
    r = {
        '/user/login': login,
        '/user/login/view': login_view,
        '/user/register': register,
        '/user/register/view': register_view,
        '/admin/update_user_password': admin_required(update_user_password),
        '/admin/edit_password': admin_required(edit_password),
    }
    return r
