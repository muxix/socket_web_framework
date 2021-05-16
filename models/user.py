from models import Model
from models.user_role import UserRole

import hashlib


class User(Model):
    """
    保存用户数据的 model
    """

    def __init__(self, form):
        super().__init__(form)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = form.get('role', UserRole.normal)

    @staticmethod
    def guest():

        form = dict(
            role=UserRole.guest,
            username='【游客】',
        )
        u = User(form)
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    @staticmethod
    def admin():
        form = dict(
            role=UserRole.admin,
            # username='【管理员】',
            # id=-10,
        )
        u = User(form)
        return u

    def is_admin(self):
        return self.role == UserRole.admin

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        """$!@><?>HUI&DWQa`"""
        salted = password + salt
        hash = hashlib.sha256(salted.encode()).hexdigest()
        return hash

    @classmethod
    def login(cls, form):
        salted = cls.salted_password(form['password'])
        u = User.find_by(username=form['username'], password=salted)
        if u is not None:
            result = '登录成功'
            return u, result
        else:
            result = '用户名或者密码错误'
            return User.guest(), result

    @classmethod
    def register(cls, form):
        valid = len(form['username']) > 2 and len(form['password']) > 2
        if valid:
            form['password'] = cls.salted_password(form['password'])
            u = User.new(form)
            result = '注册成功<br> <pre>{}</pre>'.format(u.username)
            return u, result
        else:
            result = '用户名或者密码长度必须大于2'
            return User.guest(), result

    @classmethod
    def update(cls, form, salted_pw):
        # 从表单中取到用户 id
        user_id = int(form['id'])
        # 根据用户 id 在所有用户里找到对应用户
        u = User.find_by(id=user_id)
        # 修改此用户的密码
        # u.password = form['password']
        u.password = salted_pw

        u.save()
