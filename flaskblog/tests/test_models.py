from flaskblog.models import User, Post

def test_user_model(new_user):
    """Test the User model."""
    assert new_user.username == 'newuser'
    assert new_user.email == 'newuser@example.com'

def test_post_model(test_app, new_user):
    """Test the Post model."""
    post = Post(title='Test Post', content='This is a test post.', author=new_user)
    from flaskblog import db
    db.session.add(post)
    db.session.commit()

    assert post.query.count() == 1
    assert post.author.username == 'newuser'
    assert post.title == 'Test Post'
