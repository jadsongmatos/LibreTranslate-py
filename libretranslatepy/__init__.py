"""A client library for accessing LibreTranslate"""

from .client import AuthenticatedClient, Client

__all__ = (
    "AuthenticatedClient",
    "Client",
)

from .compat import LibreTranslateAPI
