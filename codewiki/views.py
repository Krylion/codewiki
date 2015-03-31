import re
from docutils.core import publish_parts

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from pyramid.view import (
    view_config,
    forbidden_view_config,
    )

from pyramid.security import (
    remember,
    forget,
    )

from .security import USERS

from .models import (
    DBSession,
    Page,
    )


# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='view_wiki',
             permission='view')
def view_wiki(request):
    return HTTPFound(location = request.route_url('view_page',
                                                  pagename='CodeWiki'))

@view_config(route_name='search',
             permission='view')
def search(request):
    if "page" in request.POST:
        page = request.POST.get('page')
        new_str = "%"+page+"%"
        exists = DBSession.query(Page).filter(Page.name.like(new_str)).all()
        if exists:
            if len(exists) > 1:
                return HTTPFound(location = request.route_url('all_like', pagename=new_str))

            return HTTPFound(location = request.route_url('view_page', pagename=page))
        else:
            return HTTPFound(location = request.route_url('add_page', pagename=page))

    else:
        return HTTPFound(location = request.route_url('view_page', pagename='CodeWiki'))


@view_config(route_name='view_page', renderer='templates/view.pt',
             permission='view')
def view_page(request):
    pagename = request.matchdict['pagename']
    page = DBSession.query(Page).filter_by(name=pagename).first()
    #Note.query.filter(Note.message.like("%somestr%")).all()
    if page is None:
        return HTTPNotFound('Nie ma takiej strony')

    def check(match):
        word = match.group(1)
        exists = DBSession.query(Page).filter_by(name=word).all()
        if exists:
            view_url = request.route_url('view_page', pagename=word)
            return '<a href="%s">%s</a>' % (view_url, word)
        else:
            add_url = request.route_url('add_page', pagename=word)
            return '<a href="%s">%s</a>' % (add_url, word)

    content = publish_parts(page.data, writer_name='html')['html_body']
    content = wikiwords.sub(check, content)
    edit_url = request.route_url('edit_page', pagename=pagename)
    return dict(page=page, content=content, edit_url=edit_url,
                logged_in=request.authenticated_userid)

@view_config(route_name='add_page', renderer='templates/edit.pt',
             permission='edit')
def add_page(request):
    pagename = request.matchdict['pagename']
    if 'form.submitted' in request.params:
        body = request.params['body']
        page = Page(name=pagename, data=body)
        DBSession.add(page)
        return HTTPFound(location = request.route_url('view_page',
                                                      pagename=pagename))
    save_url = request.route_url('add_page', pagename=pagename)
    page = Page(name='', data='')
    return dict(page=page, save_url=save_url,
                logged_in=request.authenticated_userid)

@view_config(route_name='edit_page', renderer='templates/edit.pt',
             permission='edit')
def edit_page(request):
    pagename = request.matchdict['pagename']
    page = DBSession.query(Page).filter_by(name=pagename).one()
    if 'form.submitted' in request.params:
        page.data = request.params['body']
        DBSession.add(page)
        return HTTPFound(location = request.route_url('view_page',
                                                      pagename=pagename))
    return dict(
        page=page,
        save_url=request.route_url('edit_page', pagename=pagename),
        logged_in=request.authenticated_userid
        )

@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    login_url = request.route_url('login')
    referrer = request.url

    requrl = request.url
    info = "Brak sprecyzowanej wiadomosci"
    if "add_page" in requrl:
        info = "Wyszukiwana fraza nie zostala znaleziona. Zaloguj sie aby dodac zagadnienie do bazy CodeWiki..."
    elif "edit_page" in requrl:
        info = "Kreator edycji strony, aby kontynuowac nalezy sie zalogowac"

    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''

    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if USERS.get(login) == password:
            headers = remember(request, login)
            return HTTPFound(location = came_from,
                             headers = headers)
        message = 'Logowanie nie powiodlo sie!'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        login = login,
        password = password,
        info=info
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('view_wiki'),
                     headers = headers)

@view_config(route_name='how_to_add', renderer='templates/how_to_add.pt',
             permission='view')
def how_to_add(request):
    return dict(logged_in=request.authenticated_userid)


@view_config(route_name='all', renderer='templates/all.pt',
             permission='view')
def all(request):
    alle = DBSession.query(Page.name).order_by(Page.name).all()

    return dict(all=alle, logged_in=request.authenticated_userid)

@view_config(route_name="all_like", renderer='templates/all_like.pt',
             permission='view')
def all_like(request):
    pagename = request.matchdict['pagename']

    page = DBSession.query(Page).filter(Page.name.like(pagename)).all()

    return dict(all=page, logged_in=request.authenticated_userid)