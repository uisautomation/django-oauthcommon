"""
The :py:mod:`automationoauthclient.oauth2client` module provides a wrapper around
:py:class:`requests.Session` which is pre-authorised with an OAuth2 client token.

"""
from automationoauth.client import AuthenticatedSession as _AuthenticatedSession


class AuthenticatedSession(_AuthenticatedSession):
    pass
