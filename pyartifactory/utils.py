"""
Definition of all utils.
"""

from typing import Any, Never, Type, Tuple, Union

import requests
from pydantic import SecretStr
from pydantic.json import pydantic_encoder

from pyartifactory.exception import ArtifactoryException

logger = logging.getLogger("pyartifactory")


def custom_encoder(obj: Any) -> Any:
    """
    Custom encoder function to be passed to the default argument of json.dumps()
    :param obj: A pydantic object
    :return: An encoded pydantic object
    """
    if isinstance(obj, SecretStr):
        return obj.get_secret_value()
    return pydantic_encoder(obj)


def coerce_exception(
    error: requests.exceptions.HTTPError,
    expected_code: Union[int, Tuple[int, ...]],
    custom_error: Type[ArtifactoryException],
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
        raise custom_exception(message % tuple(args))
    raise ArtifactoryException from error