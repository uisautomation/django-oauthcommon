"""
Module providing lookup API-related functionality.

"""
import logging
from django.conf import settings
from django.core.cache import cache

from .models import UserLookup

from . import get_authenticated_session, get_person


LOG = logging.getLogger(__name__)


#: An authenticated session which can access the lookup API. Use old OAUTH2_LOOKUP_SCOPES setting
#: if provided, otherwise fall back to newer LOOKUP_OAUTH2_SCOPES.
LOOKUP_SESSION = get_authenticated_session()


class LookupError(RuntimeError):
    """
    Error raised if :py:func:`~.get_person_for_user` encounters a problem.
    """
    pass


def get_person_for_user(user):
    """
    Return the resource from Lookup associated with the specified user. A requests package
    :py:class:`HTTPError` is raised if the request fails.

    The result of this function call is cached based on the username so it is safe to call this
    multiple times.

    If user is the anonymous user (user.is_anonymous is True), :py:class:`~.UserIsAnonymousError`
    is raised.

    """
    # check that the user is not anonymous
    if user.is_anonymous:
        raise LookupError('User is anonymous')

    # return a cached response if we have it
    cached_resource = cache.get("{user.username}:lookup".format(user=user))
    if cached_resource is not None:
        return cached_resource

    # check the user has an associated lookup identity
    if not UserLookup.objects.filter(user=user).exists():
        raise LookupError('User has no lookup identity')

    # Extract the scheme and identifier for the token
    scheme = user.lookup.scheme
    identifier = user.lookup.identifier

    # Ask lookup about this person
    lookup_resource = get_person(identifier, scheme, fetch=['all_insts', 'all_groups'])

    # save cached value
    cache.set("{user.username}:lookup".format(user=user), lookup_resource,
              settings.LOOKUP_PEOPLE_CACHE_LIFETIME)

    # recurse, which should now retrieve the value from the cache
    return get_person_for_user(user)
