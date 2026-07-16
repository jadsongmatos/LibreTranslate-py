import json

from .client import AuthenticatedClient, Client as _Client
from .api.translate.post_detect import sync_detailed as _detect
from .api.translate.post_translate import sync_detailed as _translate
from .api.translate.get_languages import sync_detailed as _languages
from .api.translate.post_translate_file import sync_detailed as _translate_file
from .api.misc.get_health import sync_detailed as _health
from .api.misc.get_frontend_settings import sync_detailed as _frontend
from .api.misc.post_suggest import sync_detailed as _suggest
from .models import (
    PostDetectBody, PostTranslateBody, PostSuggestBody, PostTranslateFileBody,
)

DEFAULT_URL = "https://translate.terraprint.co/"


class LibreTranslateAPI:
    """Connect to the LibreTranslate API"""

    def __init__(self, url: str | None = None, api_key: str | None = None):
        self.url = (url or DEFAULT_URL).rstrip("/") + "/"
        self._client = AuthenticatedClient(base_url=self.url, token=api_key) if api_key else _Client(base_url=self.url)

    def translate(self, q: str, source: str = "en", target: str = "es", format: str = "text", alternatives: int = 0, timeout: int | None = None) -> str:
        body = PostTranslateBody(q=q, source=source, target=target, format_=format, alternatives=alternatives)
        return json.loads(_translate(client=self._client, body=body).content)["translatedText"]

    def detect(self, q: str, timeout: int | None = None) -> list:
        return json.loads(_detect(client=self._client, body=PostDetectBody(q=q)).content)

    def languages(self, timeout: int | None = None) -> list:
        return json.loads(_languages(client=self._client).content)

    def health(self, timeout: int | None = None) -> dict:
        return json.loads(_health(client=self._client).content)

    def frontend_settings(self, timeout: int | None = None) -> dict:
        return json.loads(_frontend(client=self._client).content)

    def suggest(self, q: str, s: str, source: str, target: str, timeout: int | None = None) -> dict:
        return json.loads(_suggest(client=self._client, body=PostSuggestBody(q=q, s=s, source=source, target=target)).content)

    def translate_file(self, file: bytes | str, source: str, target: str, timeout: int | None = None) -> dict:
        return json.loads(_translate_file(client=self._client, body=PostTranslateFileBody(file=file, source=source, target=target)).content)
