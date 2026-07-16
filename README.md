# LibreTranslate-py

Python bindings to connect to a [LibreTranslate API](https://github.com/LibreTranslate/LibreTranslate)

https://pypi.org/project/libretranslatepy/

## Install
```
pip install libretranslatepy
```

## Example usage
```python
from libretranslatepy import LibreTranslateAPI

lt = LibreTranslateAPI("https://libretranslate.com/")

print(lt.translate("LibreTranslate is awesome!", "en", "es"))
# LibreTranslate es impresionante!

print(lt.detect("Hello World"))
# [{"confidence": 0.6, "language": "en"}]

print(lt.languages())
# [{"code":"en", "name":"English"}, {"code":"es", "name":"Spanish"}]

print(lt.health())
# {"status": "ok"}

print(lt.frontend_settings())
# {"keyRequired": false, "charLimit": 500, ...}
```

## Available methods

| Method | Endpoint | Description |
|---|---|---|
| `translate(q, source, target, format, alternatives)` | `POST /translate` | Translate text |
| `detect(q)` | `POST /detect` | Detect language |
| `languages()` | `GET /languages` | List supported languages |
| `health()` | `GET /health` | Health check |
| `frontend_settings()` | `GET /frontend/settings` | Server frontend settings |
| `suggest(q, s, source, target)` | `POST /suggest` | Submit translation suggestion |
| `translate_file(file, source, target)` | `POST /translate_file` | Translate a file |

## Generate client from spec

The client is generated from the [LibreTranslate OpenAPI spec](https://libretranslate.com/spec):

```
python generate.py
```

This fetches the spec and regenerates `libretranslatepy/api.py` automatically.

## Tests

```
python -m pytest test_libretranslate.py
```

## [LibreTranslate Mirrors](https://github.com/LibreTranslate/LibreTranslate#mirrors)

## License
Licensed under either the MIT License or Public Domain

Developed by P.J. Finlay
