import pytest
import transaction
import time
from pyramid import testing

from learning_journal.models import (
    Entry,
    get_tm_session,
)
from learning_journal.models.meta import Base
from learning_journal.scripts.initializedb import ENTRIES
from pyramid.config import Configurator
import datetime

MODEL_ENTRIES = [Entry(
    title=entry['title'],
    body=entry['body'],
    creation_date=entry['creation_date']
) for entry in ENTRIES]


TEST_ENTRIES = [
    {'title': "Test 1",
     'body': 'Test body: first entry',
     'creation_date': datetime.datetime(2016, 12, 24, 0, 0),
     'id': 1},
    {'title': "Test 2",
     'body': 'Test body: second entry',
     'creation_date': datetime.datetime(2017, 1, 1, 0, 0),
     'id': 2},
    {'title': "Test 3",
     'body': 'Test body: third entry',
     'creation_date': datetime.datetime(2017, 1, 2, 0, 0),
     'id': 3},
    {'title': "Test 4",
     'body': 'Test body: fourth entry',
     'creation_date': datetime.datetime(2017, 1, 3, 0, 0),
     'id': 4},
    {'title': "Test 5",
     'body': 'Test body: fifth entry',
     'creation_date': datetime.datetime(2017, 1, 4, 0, 0),
     'id': 5},
]


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.

    This Configurator sets up a pointer to the location of the database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.
    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include(".models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session, method="GET"):
    """Instantitate an HTTP request and database session for testing"""
    request = testing.DummyRequest()
    request.method = method
    request.dbsession = db_session
    return request


def test_database_empty_but_exists(db_session):
    """Test that app connects to database, which is empty here."""
    assert len(db_session.query(Entry).all()) == 0


def test_my_view(dummy_request):
    """Test the homepage view returns data from database."""
    from .views.default import my_view
    dummy_request.dbsession.add(Entry(title="one", id='1'))
    result = my_view(dummy_request) # views commit changes to the DB
    assert result["entries"][0].title == "one"


def test_detail_view(dummy_request, db_session):
    """Test the detail view."""
    from .views.default import detail
    dummy_request.method = "POST"
    dummy_request.POST["title"] = "This is a Title"
    dummy_request.POST["body"] = "And this is the body. TEST!"
    dummy_request.matchdict['id'] = '1'
    result = detail(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(1)
    assert result['entry'] == entry
    config.include("learning_journal.models")

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture(scope="function")
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry["dbsession_factory"]
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    return session


@pytest.fixture
def add_posts(dummy_request):
    """Add multiple entries to the database."""
    for entry in TEST_ENTRIES:
            post = Entry(id=entry['id'], title=entry['title'], body=entry['body'], creation_date=entry['creation_date'])
            dummy_request.dbsession.add(post)


MODEL_ENTRIES = [Entry(
    title=entry['title'],
    body=entry['body'],
    creation_date=entry['creation_date']
) for entry in ENTRIES]


@pytest.fixture
def dummy_request(db_session, method="GET"):
    """Instantitate an HTTP request and database session for testing"""
    request = testing.DummyRequest()
    request.method = method
    request.dbsession = db_session
    return request

@pytest.fixture
def testapp(request):
    """Create an app instance for testing."""
    from webtest import TestApp
    from learning_journal import main
    app = main({})
    def main(global_config, **settings):
        """Return a Pyramid WSGI application."""
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('learning_journal.models')
        config.include('learning_journal.routes')
        config.include('learning_journal.security')
        config.scan()
        return config.make_wsgi_app()

    testapp = TestApp(app)
    session_factory = app.registry["dbsession_factory"]
    session = session_factory()
    engine = session.bind
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(tearDown)
    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Fill database with journal entries."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        for entry in ENTRIES:
            post = Entry(title=entry["title"], creation_date=entry["creation_date"], body=entry["body"])
            dbsession.add(post)
    return dbsession

def test_database_empty_but_exists(db_session):
    """Test that app connects to database, which is empty here."""
    assert len(db_session.query(Entry).all()) == 0

def test_my_view(dummy_request):
    """Test the homepage view return data from database."""
    from learning_journal.views.default import my_view
    dummy_request.dbsession.add(Entry(title="one", id='1'))
    result = my_view(dummy_request) # views commit changes to the DB
    assert result["entries"][0].title == "one"

def test_detail_view(dummy_request, db_session):
    """Test the detail view."""
    from learning_journal.views.default import detail
    dummy_request.matchdict['id'] = '1'
    result = detail(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(1)
    assert result['entry'] == entry

def test_model_gets_added(db_session):
    """Test the model gets added to the database."""
    assert len(db_session.query(Entry).all()) == 1
    model = Entry(title="new title for new test", body="new body for new test",
        creation_date=datetime.datetime(2017, 1, 1, 0, 0), id="8675309")
    db_session.add(model)
    assert len(db_session.query(Entry).all()) == 2

def test_non_authenticated_user_cannot_access_write_view(testapp):
    """Test that accessing create new post is forbidden without auth."""
    response = testapp.get('/journal/write', status=403)
    assert response.status_code == 403

def test_non_authenticated_user_cannot_access_edit_view(testapp):
    """Test that accessing create new post is forbidden without auth."""
    response = testapp.get('/journal/1/editentry', status=403)
    assert response.status_code == 403
