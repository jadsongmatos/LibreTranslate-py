import json
import unittest
from unittest.mock import patch, MagicMock
from libretranslatepy import LibreTranslateAPI


class TestLibreTranslateAPI(unittest.TestCase):
    def setUp(self):
        self.api = LibreTranslateAPI()

    def _mock_httpx(self, data, status=200):
        resp = MagicMock()
        resp.status_code = status
        resp.content = json.dumps(data).encode()
        return resp

    # --- translate ---

    @patch("libretranslatepy.compat._translate")
    def test_translate(self, mock_fn):
        mock_fn.return_value.content = json.dumps({"translatedText": "Hola mundo"}).encode()
        result = self.api.translate("Hello world", "en", "es")
        self.assertEqual(result, "Hola mundo")

    @patch("libretranslatepy.compat._translate")
    def test_translate_with_defaults(self, mock_fn):
        mock_fn.return_value.content = json.dumps({"translatedText": "Hola"}).encode()
        result = self.api.translate("Hello", "en", "es")
        self.assertEqual(result, "Hola")
        _, kwargs = mock_fn.call_args
        body = kwargs["body"]
        self.assertEqual(body.q, "Hello")
        self.assertEqual(body.source, "en")

    @patch("libretranslatepy.compat._translate")
    def test_translate_with_api_key(self, mock_fn):
        api = LibreTranslateAPI(api_key="test-key")
        mock_fn.return_value.content = json.dumps({"translatedText": "Hola"}).encode()
        result = api.translate("Hello", "en", "es")
        self.assertEqual(result, "Hola")

    # --- detect ---

    @patch("libretranslatepy.compat._detect")
    def test_detect(self, mock_fn):
        data = [{"confidence": 0.95, "language": "en"}]
        mock_fn.return_value.content = json.dumps(data).encode()
        result = self.api.detect("Hello world")
        self.assertEqual(result, data)

    # --- languages ---

    @patch("libretranslatepy.compat._languages")
    def test_languages(self, mock_fn):
        data = [{"code": "en", "name": "English"}]
        mock_fn.return_value.content = json.dumps(data).encode()
        result = self.api.languages()
        self.assertEqual(result, data)

    # --- health ---

    @patch("libretranslatepy.compat._health")
    def test_health(self, mock_fn):
        mock_fn.return_value.content = json.dumps({"status": "ok"}).encode()
        result = self.api.health()
        self.assertEqual(result, {"status": "ok"})

    # --- frontend_settings ---

    @patch("libretranslatepy.compat._frontend")
    def test_frontend_settings(self, mock_fn):
        data = {"keyRequired": False, "charLimit": 500}
        mock_fn.return_value.content = json.dumps(data).encode()
        result = self.api.frontend_settings()
        self.assertEqual(result, data)

    # --- suggest ---

    @patch("libretranslatepy.compat._suggest")
    def test_suggest(self, mock_fn):
        mock_fn.return_value.content = json.dumps({"success": True}).encode()
        result = self.api.suggest("Hello", "Hola", "en", "es")
        self.assertEqual(result, {"success": True})

    # --- translate_file ---

    @patch("libretranslatepy.compat._translate_file")
    def test_translate_file(self, mock_fn):
        data = {"translatedFileUrl": "https://example.com/translated.txt"}
        mock_fn.return_value.content = json.dumps(data).encode()
        result = self.api.translate_file(b"Hello world", "en", "es")
        self.assertIn("translatedFileUrl", result)

    # --- custom URL ---

    def test_custom_url_ensures_slash(self):
        api = LibreTranslateAPI("https://example.com")
        self.assertEqual(api.url, "https://example.com/")

        api2 = LibreTranslateAPI("https://example.com/")
        self.assertEqual(api2.url, "https://example.com/")

    # --- all methods defined ---

    def test_all_methods_defined(self):
        methods = ["translate", "detect", "languages", "health", "frontend_settings", "suggest", "translate_file"]
        for m in methods:
            self.assertTrue(hasattr(self.api, m), f"Missing method: {m}")


if __name__ == "__main__":
    unittest.main()
