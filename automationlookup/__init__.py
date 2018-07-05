"""
The :py:mod:`automationlookup` module provides functionality for integrating with the UIS
Automation Lookup proxy service.

"""
from urllib.parse import urljoin, urlencode
from django.conf import settings
from django.core.cache import cache

from automationoauth.client import AuthenticatedSession

default_app_config = 'automationlookup.apps.AutomationLookupConfig'


def get_person(identifier, scheme='crsid', fetch=None, session=None):
    """
    Return the resource from Lookup associated with the specified user. A requests package
    :py:class:`HTTPError` is raised if the request fails.

    :param str identifier: Lookup identifier for person
    :param str scheme: Lookup scheme for person
    :param list[str] fetch: List of additional attributes to fetch for the person.
    :param :py:class:`automationoauth.client.AuthenticatedSession` session: Authenticated session
       for calling Lookup proxy API.

    If *session* is ``None``, the return value from :py:func:`~.get_authenticated_session` is used.

    The result of this function call is cached based on the arguments to the call so it is safe to
    call this multiple times.

    """
    # Use default session is not specified
    session = session if session is not None else get_authenticated_session()

    # Form the key for the django cache from the identifier, scheme and id of the session object
    fetch_key = '' if fetch is None else ','.join(fetch)
    cache_key = 'lookup:get_person:{identifier}:{scheme}:{fetch_key}:{session}'.format(
        identifier=identifier, scheme=scheme, fetch_key=fetch_key, session=id(session))

    # return a cached response if we have it
    cached_resource = cache.get(cache_key)
    if cached_resource is not None:
        return cached_resource

    # Ask lookup about this person
    params = {}
    if fetch is not None and len(fetch) > 0:
        params['fetch'] = ','.join(fetch)

    endpoint = 'people/{scheme}/{identifier}'.format(
        scheme=scheme, identifier=identifier)
    if params != {}:
        endpoint += '?' + urlencode(params)

    lookup_response = session.request(
        method='GET', url=urljoin(settings.LOOKUP_ROOT, endpoint))

    # Raise if there was an error
    lookup_response.raise_for_status()

    # save cached value
    cache.set(cache_key, lookup_response.json(),
              settings.LOOKUP_RESPONSE_CACHE_LIFETIME)

    # recurse, which should now retrieve the value from the cache
    return get_person(identifier, scheme, fetch=fetch, session=session)


def get_authenticated_session():
    """
    Return a :py:mod:`automationoauth.client.AuthenticatedSession` instance pre-authenticated with
    the required OAuth2 scopes to access the lookup proxy.

    The return value is cached.

    For compatibility with the legacy API, the OAUTH2_LOOKUP_SCOPES setting is used in preference
    to LOOKUP_OAUTH2_SCOPES if it is present.

    """
    cached_session = getattr(get_authenticated_session, '_cached_session', None)
    if cached_session is not None:
        return cached_session
    scopes = getattr(settings, 'OAUTH2_LOOKUP_SCOPES', settings.LOOKUP_OAUTH2_SCOPES)
    get_authenticated_session._cached_session = AuthenticatedSession(scopes=scopes)
    return get_authenticated_session()
