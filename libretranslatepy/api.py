import json
from typing import Any
from urllib import request, parse


class LibreTranslateAPI:
    """Connect to the LibreTranslate API"""

    DEFAULT_URL = "https://translate.terraprint.co/"

    def __init__(self, url: str | None = None, api_key: str | None = None):
        self.url = LibreTranslateAPI.DEFAULT_URL if url is None else url
        self.api_key = api_key
        assert len(self.url) > 0
        if self.url[-1] != "/":
            self.url += "/"


    def detect(self, q, timeout: int | None = None):
        """Detect Language of Text"""
        url = self.url + "detect"
        params = {"q": q}
        if self.api_key is not None:
            params["api_key"] = self.api_key
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode())
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)

    def frontend_settings(self, timeout: int | None = None):
        """Retrieve Frontend Settings"""
        url = self.url + "frontend/settings"
        params = {}
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode(), method="GET")
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)

    def health(self, timeout: int | None = None):
        """Health Check"""
        url = self.url + "health"
        params = {}
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode(), method="GET")
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)

    def languages(self, timeout: int | None = None):
        """Get Supported Languages"""
        url = self.url + "languages"
        params = {}
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode(), method="GET")
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)

    def suggest(self, q, s, source, target, timeout: int | None = None):
        """Submit a Suggestion to Improve a Translation"""
        url = self.url + "suggest"
        params = {"q": q, "s": s, "source": source, "target": target}
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode())
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)

    def translate(self, q, source, target, format="text", alternatives=0, timeout: int | None = None):
        """Translate Text"""
        url = self.url + "translate"
        params = {"q": q, "source": source, "target": target, "format": format, "alternatives": alternatives}
        if self.api_key is not None:
            params["api_key"] = self.api_key
        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode())
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)["translatedText"]

    def translate_file(self, file, source, target, timeout: int | None = None):
        """Translate a File"""
        url = self.url + "translate_file"
        params = {"source": source, "target": target}
        if self.api_key is not None:
            params["api_key"] = self.api_key
        import io
        from urllib.request import Request, urlopen
        boundary = "----LibreTranslateGen" + str(hash(file))
        body = []
        for k, v in params.items():
            body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
        if isinstance(file, bytes):
            file_data = file
        elif hasattr(file, 'read'):
            file_data = file.read()
        else:
            file_data = file.encode()
        body.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"file\"\r\nContent-Type: application/octet-stream\r\n\r\n".encode())
        body.append(file_data if isinstance(file_data, bytes) else file_data.encode())
        body.append(f"\r\n--{boundary}--\r\n".encode())
        data = b"".join(body)
        req = Request(url, data=data)
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        response = urlopen(req, timeout=timeout)
        return json.loads(response.read().decode())
