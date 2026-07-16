import json
import re
import os
from urllib import request

SPEC_URL = "https://libretranslate.com/spec"
SPEC_CACHE = os.path.join(os.path.dirname(__file__), "spec.json")

HEADER = '''import json
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

'''

METHOD = '''
    def {method_name}(self, {params}):
        """{summary}"""
        url = self.url + "{path}"
        params = {{{param_dict}}}
{api_key_block}\
{body}
'''


def snake_case(name):
    name = re.sub(r'[^a-zA-Z0-9 ]', '_', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower().strip('_')


def to_python_params(parameters):
    func_params = []
    dict_items = []
    has_api_key = False
    has_file = False
    for p in parameters:
        name = p.get("name")
        if name == "api_key":
            has_api_key = True
            continue
        is_file = p.get("type") == "file"
        if is_file:
            has_file = True
        required = p.get("required", True)
        schema = p.get("schema", {})
        default = schema.get("default") if schema else p.get("default")
        if not required and default is not None:
            if isinstance(default, str):
                func_params.append(f'{name}="{default}"')
            else:
                func_params.append(f"{name}={default}")
        elif not required:
            func_params.append(f'{name}=None')
        else:
            func_params.append(name)
        if not is_file:
            dict_items.append(f'"{name}": {name}')
    return func_params, dict_items, has_api_key, has_file


def gen_get():
    return '''        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode(), method="GET")
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)'''


def gen_post():
    return '''        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode())
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)'''


def gen_post_translate():
    return '''        url_params = parse.urlencode(params)
        req = request.Request(url, data=url_params.encode())
        response = request.urlopen(req, timeout=timeout)
        response_str = response.read().decode()
        return json.loads(response_str)["translatedText"]'''


def gen_file():
    return '''        import io
        from urllib.request import Request, urlopen
        boundary = "----LibreTranslateGen" + str(hash(file))
        body = []
        for k, v in params.items():
            body.append(f"--{boundary}\\r\\nContent-Disposition: form-data; name=\\"{k}\\"\\r\\n\\r\\n{v}\\r\\n".encode())
        if isinstance(file, bytes):
            file_data = file
        elif hasattr(file, 'read'):
            file_data = file.read()
        else:
            file_data = file.encode()
        body.append(f"--{boundary}\\r\\nContent-Disposition: form-data; name=\\"file\\"; filename=\\"file\\"\\r\\nContent-Type: application/octet-stream\\r\\n\\r\\n".encode())
        body.append(file_data if isinstance(file_data, bytes) else file_data.encode())
        body.append(f"\\r\\n--{boundary}--\\r\\n".encode())
        data = b"".join(body)
        req = Request(url, data=data)
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        response = urlopen(req, timeout=timeout)
        return json.loads(response.read().decode())'''


def generate():
    print(f"Fetching spec from {SPEC_URL}...")
    try:
        resp = request.urlopen(SPEC_URL, timeout=10)
        spec = json.loads(resp.read().decode())
        with open(SPEC_CACHE, "w") as f:
            json.dump(spec, f, indent=2)
    except Exception as e:
        print(f"Download failed ({e}), trying cache...")
        if os.path.exists(SPEC_CACHE):
            with open(SPEC_CACHE) as f:
                spec = json.load(f)
        else:
            print("No cached spec found. Aborting.")
            return

    out = HEADER

    for path, methods in spec.get("paths", {}).items():
        path_clean = path.strip("/")
        for http_method, operation in methods.items():
            summary = operation.get("summary", "")
            parameters = operation.get("parameters", [])
            func_params, dict_items, has_api_key, has_file = to_python_params(parameters)

            parts = path_clean.split("/")
            method_name = "_".join(parts)
            if not method_name:
                method_name = snake_case(summary)
            method_name = snake_case(method_name)

            api_key_block = ""
            if has_api_key:
                api_key_block = "        if self.api_key is not None:\n            params[\"api_key\"] = self.api_key\n"

            params_str = ", ".join(func_params)
            if params_str:
                params_str += ", "
            params_str += "timeout: int | None = None"
            param_dict_str = ", ".join(dict_items)

            if http_method == "get":
                body = gen_get()
            elif has_file:
                body = gen_file()
            elif path_clean == "translate":
                body = gen_post_translate()
            else:
                body = gen_post()

            out += METHOD.format(
                method_name=method_name,
                summary=summary,
                params=params_str,
                path=path_clean,
                param_dict=param_dict_str if param_dict_str else "",
                api_key_block=api_key_block,
                body=body,
            )

    return out


if __name__ == "__main__":
    code = generate()
    if code:
        with open(os.path.join(os.path.dirname(__file__), "libretranslatepy", "api.py"), "w") as f:
            f.write(code)
        print("Generated libretranslatepy/api.py")
