"""Generate libretranslatepy/ from LibreTranslate spec."""
import json, os, shutil, subprocess, sys, tempfile
from urllib import request

HERE = os.path.dirname(__file__)
SPEC_FILE = os.path.join(HERE, "spec.json")
PACKAGE = os.path.join(HERE, "libretranslatepy")


def to_oai3(spec):
    def fix(s):
        if "oneOf" in s:
            for opt in s["oneOf"]:
                if isinstance(opt, dict) and opt.get("type") not in (None, "array"):
                    return {"type": opt["type"]}
            return {"type": "string"}
        if "properties" in s:
            s["properties"] = {k: fix(v) if isinstance(v, dict) else v for k, v in s["properties"].items()}
        return s

    oai = {
        "openapi": "3.0.0",
        "info": spec["info"],
        "servers": [{"url": spec.get("basePath", "/")}],
        "paths": {},
    }
    if "definitions" in spec:
        oai["components"] = {"schemas": {n: fix(dict(s)) for n, s in spec["definitions"].items()}}
    for path, ops in spec["paths"].items():
        oai["paths"][path] = {}
        for method, op in ops.items():
            op3 = {k: v for k, v in op.items() if k != "parameters"}
            form, others = [], []
            for p in op.get("parameters", []):
                (form if p.get("in") == "formData" else others).append(p)
            if others:
                op3["parameters"] = [
                    {**p, "schema": fix(p.get("schema") or {"type": p.pop("type", "string")})}
                    for p in others
                ]
            if form:
                props, required = {}, []
                for p in form:
                    n = p["name"]
                    if p.get("type") == "file":
                        props[n] = {"type": "string", "format": "binary"}
                    else:
                        props[n] = fix(p.get("schema") or {"type": p.get("type", "string")})
                    if p.get("required"):
                        required.append(n)
                ct = "multipart/form-data" if any(p.get("type") == "file" for p in form) else "application/x-www-form-urlencoded"
                op3["requestBody"] = {
                    "required": True,
                    "content": {ct: {"schema": {"type": "object", "properties": props, **({"required": required} if required else {})}}},
                }
            oai["paths"][path][method] = op3
    return oai


def main():
    if "--fetch" in sys.argv:
        resp = request.urlopen("https://libretranslate.com/spec", timeout=10)
        with open(SPEC_FILE, "wb") as f:
            f.write(resp.read())
    tmp = tempfile.mkdtemp()
    try:
        with open(SPEC_FILE) as f:
            spec = json.load(f)
        oai_path = os.path.join(tmp, "openapi.json")
        with open(oai_path, "w") as f:
            json.dump(to_oai3(spec), f)
        out_dir = os.path.join(tmp, "out")
        ret = subprocess.run(
            ["openapi-python-client", "generate", "--path", oai_path, "--output-path", out_dir],
            capture_output=True, text=True,
        )
        if ret.returncode:
            print(ret.stderr or ret.stdout)
            sys.exit(1)
        gen_pkg = next(d for d in os.listdir(out_dir) if os.path.isdir(os.path.join(out_dir, d)) and not d.startswith("."))
        shutil.rmtree(PACKAGE, ignore_errors=True)
        shutil.copytree(os.path.join(out_dir, gen_pkg), PACKAGE)
        # Add version string to __init__.py
        init = os.path.join(PACKAGE, "__init__.py")
        with open(init) as f:
            content = f.read()
        if "__version__" not in content:
            ver = spec["info"]["version"]
            # Remove old docstring, insert version after it
            _, _, rest = content.partition('"""')
            _, _, rest = rest.partition('"""')
            with open(init, "w") as f:
                f.write(f'"""A client library for accessing LibreTranslate"""\n__version__ = "{ver}"\n')
                f.write(rest)
        print("Generated libretranslatepy/")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
