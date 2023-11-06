from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import os



template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)
app.config.from_object('config')

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)


from app_blogc import models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app, name='Microblog', template_mode='bootstrap3')




class PostModelView(ModelView):
    form_columns = ['title', 'content', 'user_id', 'group_id', 'created_date', 'favorited']
    column_list = ['id', 'title', 'content', 'author', 'group', 'created_date', 'favorited']
    column_formatters = {
        'user': lambda v, c, m, p: m.user.username if m.user else '',
        'group': lambda v, c, m, p: m.group.name if m.group else '',
        'favorited': lambda v, c, m, p: len(m.favorited.all()) 
    }


class UserModelView(ModelView):
    form_columns = ['username', 'password', 'created_date', 'posts', 'groups', 'favorites']
    column_list = ['id', 'username', 'created_date', 'posts', 'groups', 'favorites']
    column_formatters = {
        'posts': lambda v, c, m, p: len(m.posts),
        'groups': lambda v, c, m, p: ', '.join([group.name for group in m.groups]),
        'favorites': lambda v, c, m, p: len(m.favorites.all()) 
    }

class GroupModelView(ModelView):
    form_columns = ['name', 'created_date', 'users', 'posts']
    column_list = ['id', 'name', 'created_date', 'users', 'posts']
    column_formatters = {
        'users': lambda v, c, m, p: ', '.join([user.username for user in m.users]),
        'posts': lambda v, c, m, p: len(m.posts)
    }

class FavoriteModelView(ModelView):
    form_columns = ['post_id', 'user_id', 'created_date']
    column_list = ['id', 'post', 'user', 'created_date']
    column_formatters = {
        'post': lambda v, c, m, p: m.post.title if m.post else '',
        'user': lambda v, c, m, p: m.user.username if m.user else ''
    }


admin.add_view(UserModelView(models.User, db.session))
admin.add_view(GroupModelView(models.Group, db.session))
admin.add_view(PostModelView(models.Post, db.session))
admin.add_view(FavoriteModelView(models.Favorite, db.session))


from app_blogc import routes_