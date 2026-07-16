import json
import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from libretranslatepy import LibreTranslateAPI


class TestLibreTranslateAPI(unittest.TestCase):
    def setUp(self):
        self.api = LibreTranslateAPI()

    def _mock_response(self, data, status=200):
        resp = MagicMock()
        resp.read.return_value = json.dumps(data).encode()
        resp.__enter__.return_value = resp
        return resp

    # --- translate ---

    @patch("urllib.request.urlopen")
    def test_translate(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"translatedText": "Hola mundo"})
        result = self.api.translate("Hello world", "en", "es")
        self.assertEqual(result, "Hola mundo")

    @patch("urllib.request.urlopen")
    def test_translate_with_api_key(self, mock_urlopen):
        api = LibreTranslateAPI(api_key="test-key")
        mock_urlopen.return_value = self._mock_response({"translatedText": "Hola"})
        result = api.translate("Hello", "en", "es")
        self.assertEqual(result, "Hola")
        req_data = mock_urlopen.call_args[0][0].data
        self.assertIn(b"api_key=test-key", req_data)

    @patch("urllib.request.urlopen")
    def test_translate_timeout(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"translatedText": "Hola"})
        self.api.translate("Hello", "en", "es", timeout=5)
        _, kwargs = mock_urlopen.call_args
        self.assertEqual(kwargs["timeout"], 5)

    # --- detect ---

    @patch("urllib.request.urlopen")
    def test_detect(self, mock_urlopen):
        mock_data = [{"confidence": 0.95, "language": "en"}]
        mock_urlopen.return_value = self._mock_response(mock_data)
        result = self.api.detect("Hello world")
        self.assertEqual(result, mock_data)

    @patch("urllib.request.urlopen")
    def test_detect_timeout(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response([])
        self.api.detect("Hello", timeout=3)
        _, kwargs = mock_urlopen.call_args
        self.assertEqual(kwargs["timeout"], 3)

    # --- languages ---

    @patch("urllib.request.urlopen")
    def test_languages(self, mock_urlopen):
        mock_data = [{"code": "en", "name": "English"}, {"code": "pt", "name": "Portuguese"}]
        mock_urlopen.return_value = self._mock_response(mock_data)
        result = self.api.languages()
        self.assertEqual(result, mock_data)

    # --- health ---

    @patch("urllib.request.urlopen")
    def test_health(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"status": "ok"})
        result = self.api.health()
        self.assertEqual(result, {"status": "ok"})

    @patch("urllib.request.urlopen")
    def test_health_uses_get(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"status": "ok"})
        self.api.health()
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.method, "GET")

    # --- frontend_settings ---

    @patch("urllib.request.urlopen")
    def test_frontend_settings(self, mock_urlopen):
        mock_data = {"keyRequired": False, "charLimit": 500}
        mock_urlopen.return_value = self._mock_response(mock_data)
        result = self.api.frontend_settings()
        self.assertEqual(result, mock_data)

    # --- suggest ---

    @patch("urllib.request.urlopen")
    def test_suggest(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"success": True})
        result = self.api.suggest("Hello", "Hola", "en", "es")
        self.assertEqual(result, {"success": True})

    @patch("urllib.request.urlopen")
    def test_suggest_params(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"success": True})
        self.api.suggest("Hello", "Hola", "en", "es")
        req_data = mock_urlopen.call_args[0][0].data
        self.assertIn(b"q=Hello", req_data)
        self.assertIn(b"s=Hola", req_data)
        self.assertIn(b"source=en", req_data)
        self.assertIn(b"target=es", req_data)

    # --- translate_file ---

    @patch("urllib.request.urlopen")
    def test_translate_file(self, mock_urlopen):
        mock_urlopen.return_value = self._mock_response({"translatedFileUrl": "https://example.com/translated.txt"})
        result = self.api.translate_file(b"Hello world", "en", "es")
        self.assertIn("translatedFileUrl", result)

    # --- custom URL ---

    def test_custom_url_ensures_slash(self):
        api = LibreTranslateAPI("https://example.com")
        self.assertEqual(api.url, "https://example.com/")

        api2 = LibreTranslateAPI("https://example.com/")
        self.assertEqual(api2.url, "https://example.com/")

    @patch("urllib.request.urlopen")
    def test_custom_url_used_in_requests(self, mock_urlopen):
        api = LibreTranslateAPI("https://custom.instance:5000")
        mock_urlopen.return_value = self._mock_response({"translatedText": "Hi"})
        api.translate("Hello", "en", "es")
        req = mock_urlopen.call_args[0][0]
        self.assertEqual(req.full_url, "https://custom.instance:5000/translate")

    # --- error handling ---

    @patch("urllib.request.urlopen")
    def test_http_error_raises(self, mock_urlopen):
        from urllib.error import HTTPError
        mock_urlopen.side_effect = HTTPError(
            url="http://example.com", code=400, msg="Bad Request", hdrs={}, fp=BytesIO(b'{"error":"invalid"}')
        )
        with self.assertRaises(HTTPError):
            self.api.translate("Hello", "en", "es")

    # --- generator: coverage for all methods ---

    def test_all_methods_defined(self):
        methods = ["translate", "detect", "languages", "health", "frontend_settings", "suggest", "translate_file"]
        for m in methods:
            self.assertTrue(hasattr(self.api, m), f"Missing method: {m}")


if __name__ == "__main__":
    unittest.main()
