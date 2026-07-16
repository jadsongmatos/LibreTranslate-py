import json, os, shutil, subprocess, sys, tempfile
from urllib import request

HERE = os.path.dirname(__file__)
PACKAGE = os.path.join(HERE, "libretranslatepy")
SPEC_PATH = os.path.join(HERE, "spec.json")


def fix(schema):
    """Replace oneOf with first primitive option."""
    if "oneOf" in schema:
        for opt in schema["oneOf"]:
            if isinstance(opt, dict) and opt.get("type") not in (None, "array"):
                return {"type": opt["type"]}
        return {"type": "string"}
    if "properties" in schema:
        schema["properties"] = {k: fix(v) if isinstance(v, dict) else v for k, v in schema["properties"].items()}
    return schema


def convert(spec):
    oai = {"openapi": "3.0.0", "info": spec["info"], "servers": [{"url": spec.get("basePath", "/")}], "paths": {}}
    for path, methods in spec.get("paths", {}).items():
        oai["paths"][path] = {}
        for method, op in methods.items():
            op3 = {k: v for k, v in op.items() if k not in ("parameters", "consumes")}
            params = op.get("parameters", [])
            form = [p for p in params if p.get("in") == "formData"]
            others = [p for p in params if p.get("in") != "formData"]
            if others:
                op3["parameters"] = []
                for p in others:
                    p3 = dict(p)
                    p3["schema"] = fix(dict(p3.pop("schema", {"type": p3.pop("type", "string")})))
                    op3["parameters"].append(p3)
            if form:
                is_file = any(p.get("type") == "file" for p in form)
                props, required = {}, []
                for p in form:
                    name = p["name"]
                    if p.get("type") == "file":
                        props[name] = {"type": "string", "format": "binary"}
                    else:
                        props[name] = fix(dict(p.get("schema", {"type": p.get("type", "string")})))
                    if p.get("required"):
                        required.append(name)
                ctype = "multipart/form-data" if is_file else "application/x-www-form-urlencoded"
                op3["requestBody"] = {
                    "required": True,
                    "content": {ctype: {"schema": {"type": "object", "properties": props, **({"required": required} if required else {})}}},
                }
            oai["paths"][path][method] = op3
    if "definitions" in spec:
        oai["components"] = {"schemas": {n: fix(dict(s)) for n, s in spec["definitions"].items()}}
    return oai


def main():
    if "--fetch" in sys.argv:
        resp = request.urlopen("https://libretranslate.com/spec", timeout=10)
        raw = json.loads(resp.read().decode())
        with open(SPEC_PATH, "w") as f:
            json.dump(raw, f, indent=2)
    with open(SPEC_PATH) as f:
        raw = json.load(f)

    tmp = tempfile.mkdtemp()
    try:
        spec_path = os.path.join(tmp, "openapi.json")
        with open(spec_path, "w") as f:
            json.dump(convert(raw), f)
        out = os.path.join(tmp, "out")
        ret = subprocess.run(
            ["openapi-python-client", "generate", "--path", spec_path, "--output-path", out],
            capture_output=True, text=True,
        )
        if ret.returncode != 0:
            print(ret.stderr or ret.stdout)
            raise SystemExit(1)
        src_name = [d for d in os.listdir(out) if os.path.isdir(os.path.join(out, d)) and not d.startswith(".")][0]
        shutil.rmtree(PACKAGE, ignore_errors=True)
        shutil.copytree(os.path.join(out, src_name), PACKAGE)
        # Write backward-compatible wrapper
        compat = '''import json

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
'''
        with open(os.path.join(PACKAGE, "compat.py"), "w") as f:
            f.write(compat)
        with open(os.path.join(PACKAGE, "__init__.py"), "a") as f:
            f.write("\nfrom .compat import LibreTranslateAPI\n")
        print("Generated libretranslatepy/")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
