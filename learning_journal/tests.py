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

# Unit tests


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
        'sqlalchemy.url': 'postgres://hotsauce@localhost:5432/learning_journal'
    })
    config.include(".models")
    config.include(".routes")

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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """Instantiate a fake HTTP Request, complete with a database session.
    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database.
    Every test that includes this fixture will add new models
     from the ENTRIES list.
    """
    for each in TEST_ENTRIES:
        model = Entry(title=each["title"], creation_date=each["creation_date"], body=each["body"])
        dummy_request.dbsession.add(model)


def test_database_empty_but_exists(db_session):
    """Test that app connects to database, which is empty here."""
    assert len(db_session.query(Entry).all()) == 0


def test_adding_model(db_session):
    """Test the model gets added to the database."""
    assert len(db_session.query(Entry).all()) == 0
    model = Entry(title="new title for test", body="new body for test",
                  creation_date=datetime.datetime(2017, 1, 1, 0, 0), id="99")
    db_session.add(model)
    assert len(db_session.query(Entry).all()) == 1


def test_homepage_returns_empty_when_empty(dummy_request):
    """Test that the list view returns no journal entries if empty."""
    from learning_journal.views.default import homepage
    result = homepage(dummy_request)
    assert len(result["entries"]) == 0


def test_homepage(dummy_request):
    """Test the homepage view returns data from database."""
    from .views.default import homepage
    dummy_request.dbsession.add(Entry(title="one", body="body 1", id='1'))
    result = homepage(dummy_request)
    assert result["entries"][0].title == "one"


def test_homepage_returns_existing_entries(dummy_request, add_models):
    """Test that the list view serves up journal entries."""
    from learning_journal.views.default import homepage
    result = homepage(dummy_request)
    assert len(result["entries"]) == len(TEST_ENTRIES)


def test_detail_page_returns_empty_when_empty(dummy_request):
    """Test that the detail view returns no objects when database empty."""
    from learning_journal.views.default import detail
    req = dummy_request
    req.matchdict = {"id": "1"}
    result = detail(req)
    assert result["entry"] is None


def test_detail_view(dummy_request, db_session):
    """Test the detail view returns requested body text."""
    from .views.default import detail
    dummy_request.method = "POST"
    dummy_request.POST["title"] = "This is a Title"
    dummy_request.POST["body"] = "And this is the body. TEST!"
    dummy_request.matchdict['id'] = '1'
    result = detail(dummy_request)
    entry = dummy_request.dbsession.query(Entry).get(1)
    assert result['entry'] == entry


def test_edit_page_updates_db(dummy_request, add_models):
    """Test that the edit view edits entries in the database."""
    from learning_journal.views.default import edit
    req = dummy_request
    req.matchdict = {"id": "3"}
    req.method = "POST"
    req.POST["title"] = "new thing"
    req.POST["creation_date"] = datetime.datetime(2017, 2, 24, 0, 0)
    req.POST["body"] = "and more new things"
    edit(req)
    new_title = dummy_request.dbsession.query(Entry).get(3).title
    assert new_title == "new thing"


def test_write_view_updates_db(dummy_request, add_models):
    """Test that the write view adds entries to the database."""
    from learning_journal.views.default import write
    row_count_before_post = dummy_request.dbsession.query(Entry).count()
    req = dummy_request
    req.method = "POST"
    req.POST["title"] = "a new post"
    req.POST["title1"] = "a new subtitle"
    req.POST["creation_date"] = datetime.datetime(2016, 12, 20, 0, 0)
    req.POST["body"] = "a new body"
    try:
        write(req)
    except:
        row_count_after_post = dummy_request.dbsession.query(Entry).count()
        assert row_count_after_post == row_count_before_post + 1



#Functional tests.

@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes.
    With the alchemy scaffold we need to add to our test application the
    setting for a database to be used for the models.
    We have to then set up the database by starting a database session.
    Finally we have to create all of the necessary tables that our app
    normally uses to function.
    The scope of the fixture is function-level, so every test will get a new
    test application.
    """
    from webtest import TestApp
    from learning_journal import main

    app = main({}, **{'sqlalchemy.url': 'sqlite:///:memory:'})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Fill database with journal entries."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        for entry in TEST_ENTRIES:
            post = Entry(title=entry["title"], creation_date=entry["creation_date"], body=entry["body"])
            dbsession.add(post)
    return dbsession


@pytest.fixture
def set_auth_credentials():
    """Make a username, password for testing."""
    import os
    from passlib.apps import custom_app_context as pwd_context

    os.environ["AUTH_USERNAME"] = "tastetest"
    os.environ["AUTH_PASSWORD"] = pwd_context.hash("Frank'sRedHot")


def test_user_can_log_in(set_auth_credentials, testapp):
    """Test that a user can log in with correct credentials."""
    testapp.post("/login", params={
        "username": "tastetest",
        "password": "Frank'sRedHot"
    })
    assert "auth_tkt" in testapp.cookies


def test_anonymous_user_cant_hit_write_view(testapp):
    """Test that non-authorised users can't access write page."""
    response = testapp.get('/journal/write', status=403)
    assert response.status_code == 403


def test_anonymous_user_cant_hit_edit_view(testapp):
    """Test that nonauthorised users can't edit posts."""
    response = testapp.get('/journal/1/editentry', status=403)
    assert response.status_code == 403


def test_check_credentials_passes_with_good_creds(set_auth_credentials):
    """Test that check credentials works with valid creds."""
    from learning_journal.security import check_credentials
    assert check_credentials("tastetest", "Frank'sRedHot")


def test_check_credentials_fails_with_bad_password(set_auth_credentials):
    """Test that check credential fails on bad password."""
    from learning_journal.security import check_credentials
    assert not check_credentials("tastetest", "badpass")


def test_check_credentials_fails_with_bad_username(set_auth_credentials):
    """Test that check credential fails on bad username."""
    from learning_journal.security import check_credentials
    assert not check_credentials("Crystal", "Frank'sRedHot")


def test_list_view_shows_entries(testapp, fill_the_db):
    """Test that list view has test entries showing."""
    response = testapp.get("/")
    html = response.html
    assert b"Test 1" in response.body


def test_list_view_shows_correct_no_of_entries(testapp, fill_the_db):
    """Test that list view has test entries showing."""
    response = testapp.get("/")
    html = response.html
    assert len(TEST_ENTRIES) == len(html.findAll("article"))


def test_user_can_add_new_entry(set_auth_credentials, testapp):
    """Test that logged-in user can write a new journal entry."""
    testapp.post("/login", params={
        "username": "tastetest",
        "password": "Frank'sRedHot"
    })
    response = testapp.get('/journal/write')
    html = response.html
    csrf_token = html.find_all('input')[0]['value']
    testapp.post('/journal/write', params={
        'title': "gonna test for this", 'body': "new body", 'csrf_token': csrf_token},
        status=302)
    next_response = testapp.get("/")
    html = next_response.html
    assert b'gonna test for this' in html.findAll('h2')[0].encode()


def test_user_can_edit_entry(set_auth_credentials, testapp, fill_the_db):
    """Test that logged-in user can edit a journal entry."""
    testapp.post("/login", params={
        "username": "tastetest",
        "password": "Frank'sRedHot"
    })
    response = testapp.get('/journal/1/editentry')
    html = response.html
    csrf_token = html.findAll('input')[0]['value']
    testapp.post('/journal/1/editentry', params={
        'title': "gonna test for this", 'body': "new body", 'csrf_token': csrf_token},
        status=302)
    next_response = testapp.get("/journal/1")
    html = next_response.html
    assert b'gonna test for this' in html.findAll('h1')[1].encode()

def test_logging_in_redirects_home(set_auth_credentials, testapp):
    """Test that user redirected to home after logging in."""
    response = testapp.post("/login", params={
        "username": "tastetest",
        "password": "Frank'sRedHot"
    })
    assert response.status_code == 302
    assert response.follow().status_code == 200


def test_bad_login_refreshes(set_auth_credentials, testapp):
    """Test that user redirected to home after logging in."""
    response = testapp.post("/login", params={
        "username": "tastetest",
        "password": "notahotsauce"
    })
    assert response.status_code == 200


def test_logging_out_redircts_home(set_auth_credentials, testapp):
    """Test that user redirected to home after logging out."""
    testapp.post("/login", params={
        "username": "tastetest",
        "password": "Frank'sRedHot"
    })
    response = testapp.get('/logout')
    assert response.status_code == 302



def test_user_can_add_new_entry(set_auth_credentials, testapp):
    """Test that logged-in user can write a new journal entry."""
    testapp.post("/login", params={
        "username": "tastetest",
        "password": "Frank'sRedHot"
    })
    response = testapp.get('/journal/write')
    html = response.html
    csrf_token = html.find_all('input')[0]['value']
    testapp.post('/journal/write', params={
        'title': "gonna test for this", 'body': "new body", 'csrf_token': csrf_token},
        status=302)
    next_response = testapp.get("/")
    html = next_response.html
    assert b'gonna test for this' in html.findAll('h2')[0].encode()
