def test_account_page_access(logged_in_client):
    """Test access to the account page for logged-in users."""
    response = logged_in_client.get('/account')
    assert response.status_code == 200
    assert b'Manage your account' in response.data

def test_account_update(logged_in_client):
    """Test updating account information."""
    response = logged_in_client.post(
        '/account',
        data = {'username': 'updateduser', 'email': 'updateduser@example.com'},
        follow_redirects=True
    )
    assert b'Your account has been updated' in response.data
