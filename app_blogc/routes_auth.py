from flask import jsonify, make_response, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app_blogc import app, db
from app_blogc.models import Group, User
import jwt
from datetime import datetime, timedelta
from functools import wraps, update_wrapper



def token_required(required=True):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get('token')
            current_user = None
            if token:
                try:
                    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                    current_user = User.query.filter_by(id=data['user_id']).first()
                except jwt.ExpiredSignatureError:
                    if required:
                        return jsonify({'message': 'Token has expired!'}), 401
                except:
                    if required:
                        return jsonify({'message': 'Token is invalid!'}), 401
            result =  f(current_user=current_user, *args, **kwargs)
            return result
        return decorated
    return wrapper


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['input_login']
        password = request.form['input_password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('token', token, httponly=True, secure=True)

            return resp
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))

    return render_template('_login.html')   


@app.route('/logout')
@token_required(required=True)
def logout(current_user):
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('token', '', expires=0)
    flash('You have been logged out', 'info')
    return resp


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        groups = Group.query.all()
        return render_template('_register.html', groups=groups)
    
    if request.method == 'POST':
        username = request.form['input_login']
        password = request.form['input_password']
        group_ids = request.form.get('groupSelect') 

        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            for group_id in group_ids:
                group = Group.query.get(group_id)
                if group:
                    new_user.groups.append(group)

            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. You can now sign in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.', 'danger')
        return render_template('_register.html')
