"""
Definition of all exceptions.
"""

import logging
from typing import Never, Tuple, Union

import requests


logger = logging.getLogger("pyartifactory")


class ArtifactoryException(Exception):
    """Generic artifactory exception."""

    @classmethod
    def raise_from(
        cls,
        error: requests.exceptions.HTTPError,
        expected_code: Union[int, Tuple[int, ...]],
        message: str,
        *args
    ) -> Never:
        """
        Coerce an HTTP response to a custom exception type
        """
        if type(expected_code) is int:
            expected_code = (expected_code,)
        if error.response.status_code in expected_code:
            logger.error(message, *args)
            raise cls(message % tuple(args))
        raise ArtifactoryException from error


class UserAlreadyExistsException(ArtifactoryException):
    """User already exists."""


class GroupAlreadyExistsException(ArtifactoryException):
    """Group already exists."""


class RepositoryAlreadyExistsException(ArtifactoryException):
    """Repository already exists."""


class PermissionAlreadyExistsException(ArtifactoryException):
    """Permission already exists."""


class UserNotFoundException(ArtifactoryException):
    """The user was not found."""


class GroupNotFoundException(ArtifactoryException):
    """The group was not found."""


class RepositoryNotFoundException(ArtifactoryException):
    """The repository was not found."""


class PermissionNotFoundException(ArtifactoryException):
    """A permission object was not found."""


class ArtifactNotFoundException(ArtifactoryException):
    """An artifact was not found"""


class BadPropertiesException(ArtifactoryException):
    """Property value includes invalid characters"""


class PropertyNotFoundException(ArtifactoryException):
    """All requested properties were not found"""


class InvalidTokenDataException(ArtifactoryException):
    """The token contains invalid data."""
