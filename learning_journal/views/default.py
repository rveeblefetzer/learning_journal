from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import exception_response
from pyramid.security import remember, forget
from learning_journal.security import check_credentials
import datetime
from ..models import Entry


@view_config(route_name='login', renderer='../templates/login.jinja2', require_csrf=False)
def login_view(request):
    """Handle the login view."""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                location=request.route_url("homepage"),
                headers=auth_head
            )

    return {}


@view_config(route_name='logout')
def logout_view(request):
    """Handle logging the user out."""
    headers = forget(request)
    return HTTPFound(request.route_url("homepage"), headers=headers)


@view_config(route_name='homepage', renderer='../templates/index.jinja2')
def homepage(request):
    """View for homepage, listing journal entries from database."""
    entries = request.dbsession.query(Entry).all()
    return {'entries': entries}


@view_config(route_name="write", renderer="../templates/write.jinja2", permission="amend")
def write(request):
    """View for creating a new journal entry."""
    if request.method == "POST":
        if request.POST["title"] and request.POST["body"]:
            new_title = request.POST["title"]
            new_body = request.POST["body"]
            new_date = datetime.date.today()
            new_entry = Entry(title=new_title, body=new_body, creation_date=new_date)

            request.dbsession.add(new_entry)
            return HTTPFound(location=request.route_url('homepage'))
        else:
            return HTTPFound(location=request.route_url('write'))
    return {}


@view_config(route_name="detail", renderer="../templates/entry.jinja2")
def detail(request):
    """View for individual entry."""
    query = request.dbsession.query(Entry)
    the_entry = query.filter(Entry.id == request.matchdict['id']).first()
    return {"entry": the_entry}


@view_config(route_name="edit", renderer="../templates/editentry.jinja2", permission="amend")
def edit(request):
    """View for page for editing entries, displaying a form."""
    the_id = request.matchdict["id"]
    entry = request.dbsession.query(Entry).get(the_id)
    if request.method == "POST":
        entry.title = request.POST["title"]
        entry.body = request.POST["body"]

        request.dbsession.flush()
        return HTTPFound(request.route_url("homepage"))
    return {"entry": entry}

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
