from django.conf import settings
from django.db import models


class UserLookup(models.Model):
    """
    A mapping from Django users to lookup schemes and identifiers.

    """
    #: The corresponding user. Since each use only has one token identity, this is a OneToOneField.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,
        related_name='lookup')

    #: The lookup identifier scheme property for the user
    scheme = models.CharField(max_length=255)

    #: The lookup identifier identifier property for the user
    identifier = models.CharField(max_length=255)
