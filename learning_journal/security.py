import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow
from pyramid.security import Everyone, Authenticated
from passlib.apps import custom_app_context as pwd_context
from pyramid.session import SignedCookieSessionFactory


class TheRoot(object):
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'amend'),
        (Allow, Everyone, 'view'),
    ]


def check_credentials(username, password):
    """Return True if correct username and password, else False."""
    stored_username = os.environ.get('AUTH_USERNAME', '')
    stored_password = os.environ.get('AUTH_PASSWORD', '')
    is_authenticated = False
    if stored_username and stored_password:
        if username == stored_username:
            try:
                is_authenticated = pwd_context.verify(password, stored_password)
            except ValueError:
                # ValueError is raised if the stored password is not hashed or if the salt is improper
                pass
    return is_authenticated

def includeme(config):
    """Pyramid security configuration."""
    auth_secret = os.environ.get("AUTH_SECRET", "hotsauce")
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg="sha512"
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_root_factory(TheRoot)
    config.set_default_permission('view')
    session_secret = os.environ.get('SESSION_SECRET', 'Louisiana')
    session_factory = SignedCookieSessionFactory(session_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)

