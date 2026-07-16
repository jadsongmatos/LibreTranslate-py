# LibreTranslate-py

Python bindings to connect to a [LibreTranslate API](https://github.com/LibreTranslate/LibreTranslate)

**100% generated from the [OpenAPI spec](https://libretranslate.com/spec).**  
No hand-written client code. When the API changes, just regenerate.

## Install

```bash
pip install libretranslatepy
```

## Usage

```python
import json
from libretranslatepy import Client
from libretranslatepy.models import PostDetectBody
from libretranslatepy.api.translate import post_detect

client = Client(base_url="https://libretranslate.com/")
resp = post_detect.sync_detailed(client=client, body=PostDetectBody(q="Hello world"))
print(json.loads(resp.content))
```

Every endpoint provides both `sync_detailed()` and `asyncio_detailed()` functions.  
See `libretranslatepy/api/` for the full list.

## Generate

```bash
pip install openapi-python-client
python generate.py              # generate from cached spec
python generate.py --fetch      # download latest spec first
```

Regenerates the entire `libretranslatepy/` package with typed models, sync/async clients, and full endpoint coverage.

```bash
python -m pytest test_libretranslate.py
```

## License

MIT or Public Domain

Developed by P.J. Finlay
