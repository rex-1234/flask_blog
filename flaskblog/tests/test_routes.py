def test_home_page(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200

def test_about_page(client):
    """Test the about page route."""
    response = client.get('/about')
    assert response.status_code == 200
