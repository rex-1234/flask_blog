from flaskblog.models import Post

def test_create_post(logged_in_client):
    """Test the post creation route."""
    response = logged_in_client.post(
        '/post/new',
        data = {'title': 'New Post', 'content': 'New post content.'},
        follow_redirects=True
    )
    assert b'Your post has been created' in response.data

def test_update_post(logged_in_client, new_user):
    """Test the post update route."""
    from flaskblog import db
    # First, create a post to update
    post = Post(title='Old Title', content='Old content.', author=new_user)
    db.session.add(post)
    db.session.commit()

    post = db.session.get(Post, post.id)

    response = logged_in_client.post(
        f'/post/{post.id}/update',
        data = {'title': 'Updated Title', 'content': 'Updated content.'},
        follow_redirects=True
    )
    assert b'Your post has been updated!' in response.data

def test_delete_post(logged_in_client, new_user):
    """Test the post deletion route."""
    from flaskblog import db
    # First, create a post to update
    post = Post(title='Detle Post', content='To Delete post content.', author=new_user)
    db.session.add(post)
    db.session.commit()

    post = db.session.get(Post, post.id)

    response = logged_in_client.post(
        f'/post/{post.id}/delete',
        follow_redirects=True
    )
    assert b'Your post has been deleted' in response.data
