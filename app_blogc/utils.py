from flask import url_for
from app_blogc.models import User, Post, Group, association_table


def get_categories(current_user):
    if current_user:
        user_groups = Group.query.join(association_table).join(User).filter(association_table.c.user_id == current_user.id).all()
        categories = [{'name': group.name, 'url': f'group/{group.id}'} for group in user_groups]
        categories.append({'name': 'My', 'url': 'my_posts'})
        categories.append({'name': 'Favs', 'url': 'my_favs'})
    else:
        categories = []
    categories.insert(0, {'name': 'All', 'url': ''})
    return categories

