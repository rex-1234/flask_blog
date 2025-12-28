import pytest
from flaskblog import create_app, db, bcrypt
from flaskblog.models import User
from flaskblog.config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    MAIL_SUPRESS_SEND = True

@pytest.fixture(scope='function')
def test_app():
    """Create and configure a new app instance for each test."""
    app = create_app(config_class=TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    """A test client for the app."""
    return test_app.test_client()

@pytest.fixture
def runner(test_app):
    """A test runner for the app's Click commands."""
    return test_app.test_cli_runner()

@pytest.fixture
def new_user(test_app):
    """Create a new user for testing."""
    user = User(
        username='newuser',
        email='newuser@example.com',
        password=bcrypt.generate_password_hash('password').decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def logged_in_client(client, new_user):
    """A test client logged in as new_user."""
    client.post(
        '/login',
        data={'email': 'newuser@example.com', 'password': 'password'},
        follow_redirects=True
    )
    return client
