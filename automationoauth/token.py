"""
The :py:mod:`automationoauth.token` module provides support for verifying and
introspecting tokens returned from the UIS Automation OAuth2 deployment.

The response from the introspect endpoint is documented in the `Hydra API
documentation <https://www.ory.sh/docs/api/hydra/?version=v0.11.12>`_.

"""

import datetime
import logging
from django.conf import settings

from . import client

LOG = logging.getLogger(__name__)


def verify_token(token, session=None):
    """
    Validate an OAuth2 token and returns the parsed response from the
    introspection endpoint if the token is valid. If the token is invalid,
    InvalidTokenError is raised.

    A valid token must be active, be issued in the past and expire in the
    future. Note that a valid token may still lack a subject.

    :param str token: Token to verify
    :param :py:class:`automationoauth.client.AuthenticatedSession` session: Authenticated session
       for calling Lookup proxy API.

    If *session* is ``None``, the return value of
    :py:func:`get_authenticated_session` will be used.

    """
    session = session if session is not None else get_authenticated_session()
    r = session.request(method='POST', url=settings.OAUTH2_INTROSPECT_URL,
                        timeout=2, data={'token': token})
    r.raise_for_status()
    token = r.json()
    if not token.get('active', False):
        raise InvalidTokenError('subject is not active')

    # Get "now" in UTC
    now = _utc_now()

    if token['iat'] > now:
        LOG.warning('Rejecting token with "iat" in the future: %s with now = %s"',
                    token['iat'], now)
        raise InvalidTokenError('token is from the future')

    if token['exp'] < now:
        LOG.warning('Rejecting token with "exp" in the past: %s with now = %s"',
                    token['exp'], now)
        raise InvalidTokenError('token has expired')

    return token


class InvalidTokenError(ValueError):
    """
    The passed token was invalid. The *reason* property is a human readable
    string describing the reason why the token was invalid.

    """
    @property
    def reason(self):
        try:
            return self.args[0]
        except IndexError:
            return ''


def get_authenticated_session():
    """Return a :py:class:`requests.Session` object authenticated to introspect
    tokens. The return value is cached.

    """
    cached_session = getattr(get_authenticated_session, '_cached', None)
    if cached_session is not None:
        return cached_session
    get_authenticated_session._cached = client.AuthenticatedSession(
        scopes=settings.OAUTH2_INTROSPECT_SCOPES)
    return get_authenticated_session()


def _utc_now():
    """Return a UNIX-style timestamp representing "now" in UTC."""
    return (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
