import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Entry

ENTRIES = [
        {"id": 1, "title": "'Drinking from a firehose'", "creation_date": "12/25/2016", "body": "After faceplanting on servers, here's Pyramid."},
        {"id": 2, "title": "Spending the time.", "creation_date": "12/26/2016", "body": "Reading, and doing."},
        {"id": 3, "title": "Getting it together.", "creation_date": "12/27/2016", "body": "Making headway with Pyramid."},
        {"id": 4, "title": "Letting it jell.", "creation_date": "12/28/2016", "body": "Making it solid."},
        {"id": 5, "title": "Moving on and building", "creation_date": "12/29/2016", "body": "Wrapping this, and getting ready for databases."},
    ]


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings["sqlalchemy.url"] = 'sqlite:///%(here)s/learning_journal.sqlite'
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]


    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        for entry in ENTRIES:
            new_entry = Entry(title=entry['title'], body=entry['body'], creation_date=entry['creation_date'])

        dbsession.add(new_entry)

