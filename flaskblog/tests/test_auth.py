def test_register(client):
    """Test the user registeration route."""
    response = client.post(
        '/register',
        data = {
            'username': 'dummyuser',
            'email': 'dummyuser@example.com',
            'password': 'password',
            'confirm_password': 'password'
        },
        follow_redirects=True
    )
    assert b"Your account has been created" in response.data

def test_login(client, new_user):
    """Test the user login route."""
    response = client.post(
        '/login',
        data = {'email': 'newuser@example.com', 'password': 'password'},
        follow_redirects=True
    )
    assert b"Logout" in response.data

def test_logout(logged_in_client):
    """Test the user logout route."""
    response = logged_in_client.get('/logout', follow_redirects=True)
    assert b"Login" in response.data
