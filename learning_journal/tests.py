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

MODEL_ENTRIES = [Entry(
    title=entry['title'],
    body=entry['body'],
    creation_date=entry['creation_date']
) for entry in ENTRIES]

@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
        database.
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


def test_write_view(dummy_request, db_session):
    """Test the write view writes to database."""
    from .views.default import write
    dummy_request.method = "POST"
    dummy_request.POST["title"] = "This is a Title"
    dummy_request.POST["body"] = "And this is the body. TEST!"

    write(dummy_request)
    query = db_session.query(Entry).all()
    assert query[0].title == "This is a Title"
    assert query[0].body == "And this is the body. TEST!"


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


