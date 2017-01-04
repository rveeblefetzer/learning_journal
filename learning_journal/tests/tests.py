"""Tests for learning journal app, built with Pyramid and Postgres."""

import pytest
import transaction
from pyramid import testing
from pyramid.config import Configurator
import time

from learning_journal.models import (
    Entry,
    get_tm_session,
)
from learning_journal.models.meta import Base

TEST_ENTRIES = [
    {'title': "Test 1",
     'body': 'Test body: first entry',
     'creation_date': '12/31/2016',
     'id': 1},
    {'title': "Test 2",
     'body': 'Test body: second entry',
     'creation_date': '1/1/2107',
     'id': 2},
    {'title': "Test 3",
     'body': 'Test body: third entry',
     'creation_date': '1/2/2107',
     'id': 3},
    {'title': "Test 4",
     'body': 'Test body: fourth entry',
     'creation_date': '1/3/2107',
     'id': 4},
    {'title': "Test 5",
     'body': 'Test body: fifth entry',
     'creation_date': '1/4/2107',
     'id': 5},
]


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator sets up a pointer to the location of the database.
    It also includes the models from your app's model package.
    Finally it tears everything down, including the in-memory SQLite database.
    This configuration will persist for the entire duration of your PyTest run.
    """
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
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

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_posts(dummy_request):
    """Add multiple entries to the database."""
    for entry in TEST_ENTRIES:
            post = Entry(id=entry['id'], title=entry['title'], body=entry['body'], creation_date=entry['creation_date'])
            dummy_request.dbsession.add(post)

"""Tests:"""


def test_model_gets_added(db_session, add_posts):
    """Test the model gets added to the database."""
    assert len(db_session.query(Entry).all()) == 5
    model = Entry(title="new title for new test", body="new body for new test",
        creation_date="test time!", id="8675309")
    db_session.add(model)
    assert len(db_session.query(Entry).all()) == 6
#

# def test_homepage_response(add_posts):
#     """Test that homepage request gets OK response code 200."""
#     assert request.response.status = 200



# class TestMyViewSuccessCondition(BaseTest):

#     def setUp(self):
#         super(TestMyViewSuccessCondition, self).setUp()
#         self.init_database()

#         from .models import MyModel

#         model = MyModel(name='one', value=55)
#         self.session.add(model)

#     def test_passing_view(self):
#         from .views.default import my_view
#         info = my_view(dummy_request(self.session))
#         self.assertEqual(info['one'].name, 'one')
#         self.assertEqual(info['project'], 'learning_journal')


# class TestMyViewFailureCondition(BaseTest):

#     def test_failing_view(self):
#         from .views.default import my_view
#         info = my_view(dummy_request(self.session))
#         self.assertEqual(info.status_int, 500)
