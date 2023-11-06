import pytest
from app_blogc import app, db
from app_blogc.models import User, Post




@pytest.fixture(scope='module')
def test_client():
    with app.app_context():
        yield app.test_client()



@pytest.fixture(scope='module')
def init_database():
    with app.app_context():
        db.create_all()

        user1 = User(username='testuser', password='testpassword')
        user2 = User(username='testuser2', password='testpassword2')
        db.session.add(user1)
        db.session.add(user2)

        db.session.commit()

        post1 = Post(title='Test Post 1', content='Test Content 1', user_id=user1.id)
        post2 = Post(title='Test Post 2', content='Test Content 2', user_id=user2.id)
        db.session.add(post1)
        db.session.add(post2)

        db.session.commit()

        yield 

        db.drop_all()
        db.session.commit()



@pytest.fixture(scope='function')
def session(init_database):
    """Creates a new database session for a test."""
    db.session.begin_nested()

    yield db.session

    db.session.rollback()
    db.session.remove()



def test_create_user(session, init_database):
    existing_user = session.query(User).filter_by(username='new_user').first()
    if existing_user:
        session.delete(existing_user)
        session.commit()

    user = User(username='new_user', password='new_password')
    session.add(user)
    session.commit()




def test_create_post(session, init_database):
    user = session.query(User).filter_by(username='testuser').first()
    assert user is not None

    post = Post(title='New Post', content='New Content', user_id=user.id)
    session.add(post)
    session.commit()
    
    found_post = session.query(Post).filter_by(title='New Post').first()
    assert found_post is not None



def test_update_post(session, init_database):
    post = session.query(Post).filter_by(title='New Post').first()
    assert post is not None
    
    post.title = 'Updated Post'
    session.commit()
    
    updated_post = session.query(Post).filter_by(title='Updated Post').first()
    assert updated_post is not None



def test_delete_post(session, init_database):
    post = session.query(Post).filter_by(title='Updated Post').first()
    assert post is not None
    
    session.delete(post)
    session.commit()
    
    deleted_post = session.query(Post).filter_by(title='Updated Post').first()
    assert deleted_post is None



def test_user_profile_update(session, init_database):
    user = session.query(User).filter_by(username='testuser').first()
    assert user is not None

    user.username = 'updated_username'
    session.commit()

    updated_user = session.query(User).filter_by(username='updated_username').first()
    assert updated_user is not None

