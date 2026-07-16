import json
import unittest
from io import BytesIO
from unittest.mock import patch, MagicMock
from libretranslatepy import Client
from libretranslatepy.types import File
from libretranslatepy.api.translate.post_detect import sync_detailed as detect
from libretranslatepy.api.translate.post_translate import sync_detailed as translate
from libretranslatepy.api.translate.get_languages import sync_detailed as languages
from libretranslatepy.api.translate.post_translate_file import sync_detailed as translate_file
from libretranslatepy.api.misc.get_health import sync_detailed as health
from libretranslatepy.api.misc.get_frontend_settings import sync_detailed as frontend_settings
from libretranslatepy.api.misc.post_suggest import sync_detailed as suggest
from libretranslatepy.models import (
    PostDetectBody,
    PostTranslateBody,
    PostTranslateBodyFormat,
    PostSuggestBody,
    PostTranslateFileBody,
)


def _mkresp(data, status=200):
    r = MagicMock()
    r.status_code = status
    r.content = json.dumps(data).encode()
    return r


class TestGeneratedClient(unittest.TestCase):
    def setUp(self):
        self.client = Client(base_url="https://libretranslate.com/")

    # --- translate ---

    @patch("httpx.Client.request")
    def test_translate(self, mock_req):
        mock_req.return_value = _mkresp({"translatedText": "Hola mundo"})
        body = PostTranslateBody(q="Hello world", source="en", target="es", format_=PostTranslateBodyFormat.TEXT, alternatives=0)
        resp = translate(client=self.client, body=body)
        self.assertEqual(json.loads(resp.content)["translatedText"], "Hola mundo")

    # --- detect ---

    @patch("httpx.Client.request")
    def test_detect(self, mock_req):
        data = [{"confidence": 0.95, "language": "en"}]
        mock_req.return_value = _mkresp(data)
        resp = detect(client=self.client, body=PostDetectBody(q="Hello"))
        self.assertEqual(json.loads(resp.content), data)

    # --- languages ---

    @patch("httpx.Client.request")
    def test_languages(self, mock_req):
        data = [{"code": "en", "name": "English"}]
        mock_req.return_value = _mkresp(data)
        resp = languages(client=self.client)
        self.assertEqual(json.loads(resp.content), data)

    # --- health ---

    @patch("httpx.Client.request")
    def test_health(self, mock_req):
        mock_req.return_value = _mkresp({"status": "ok"})
        resp = health(client=self.client)
        self.assertEqual(json.loads(resp.content), {"status": "ok"})

    # --- frontend_settings ---

    @patch("httpx.Client.request")
    def test_frontend_settings(self, mock_req):
        data = {"keyRequired": False}
        mock_req.return_value = _mkresp(data)
        resp = frontend_settings(client=self.client)
        self.assertEqual(json.loads(resp.content), data)

    # --- suggest ---

    @patch("httpx.Client.request")
    def test_suggest(self, mock_req):
        mock_req.return_value = _mkresp({"success": True})
        body = PostSuggestBody(q="Hello", s="Hola", source="en", target="es")
        resp = suggest(client=self.client, body=body)
        self.assertEqual(json.loads(resp.content), {"success": True})

    # --- translate_file ---

    @patch("httpx.Client.request")
    def test_translate_file(self, mock_req):
        data = {"translatedFileUrl": "https://example.com/translated.txt"}
        mock_req.return_value = _mkresp(data)
        body = PostTranslateFileBody(
            file=File(payload=BytesIO(b"Hello world"), file_name="doc.txt", mime_type="text/plain"),
            source="en",
            target="es",
        )
        resp = translate_file(client=self.client, body=body)
        self.assertIn("translatedFileUrl", json.loads(resp.content))

    # --- verifies version attribute ---

    def test_version_exists(self):
        from libretranslatepy import __version__
        self.assertIsInstance(__version__, str)

    # --- verifies Client can be created ---

    def test_client_creation(self):
        c = Client(base_url="https://example.com/")
        self.assertEqual(c._base_url, "https://example.com/")

    def test_client_creation_with_trailing_slash(self):
        c = Client(base_url="https://example.com")
        self.assertEqual(c._base_url, "https://example.com")


if __name__ == "__main__":
    unittest.main()
