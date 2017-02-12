from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import exception_response
import time

from sqlalchemy.exc import DBAPIError

from ..models import Entry


@view_config(route_name='homepage', renderer='../templates/index.jinja2')
def my_view(request):
    """View for homepage, listing journal entries from database."""
    try:
        entries = request.dbsession.query(Entry).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': entries}


@view_config(route_name="write", renderer="../templates/write.jinja2")
def write(request):
    if request.method == "POST":
        new_title = request.POST["title"]
        new_body = request.POST["body"]
        new_date = time.strftime("%m/%d/%Y")
        new_entry = Entry(title=new_title, body=new_body, creation_date=new_date)

        request.dbsession.add(new_entry)

        return {}
    return {}


@view_config(route_name="detail", renderer="../templates/entry.jinja2")
def detail(request):
    """VIew for individual entry."""
    query = request.dbsession.query(Entry)
    the_entry = query.filter(Entry.id == request.matchdict['id']).first()
    return {"entry": the_entry}


@view_config(route_name="edit", renderer="../templates/editentry.jinja2")
def edit(request):
    """View for page for editing entries, displaying a form."""
    try:
        data = request.dbsession.query(Entry).get(request.matchdict['id'])
        if request.method == "POST":
            title = request.POST['title']
            body = request.POST['body']
            creation_date = time.strftime("%m/%d/%Y")
            query = request.dbsession.query(Entry)
            post_dict = query.filter(Entry.id == request.matchdict['id'])
            post_dict.update({'title': title, 'body': body, 'creation_date': creation_date})
            return HTTPFound(location=request.route_url('homepage'))
        return {'entries': data}
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    # query = request.dbsession.query(Entry)
    # post_dict = query.filter(Entry.id == request.matchdict['id']).first()
    # if post_dict is not None:
    #     edited_post = {
    #         'title': post_dict.title,
    #         'creation_date': post_dict.creation_date,
    #         'body': post_dict.body}
    #     return {'post': edited_post}
    # raise exception_response(404)


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
