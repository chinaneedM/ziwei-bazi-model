#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, gzip, json
from pathlib import Path

def load(path: Path):
    if path.name.endswith(".json.gz.b64"):
        raw = gzip.decompress(base64.b64decode(path.read_text(encoding="utf-8").strip()))
        return json.loads(raw.decode("utf-8"))
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("bundle")
    p.add_argument("--output")
    a=p.parse_args()
    obj=load(Path(a.bundle))
    body=json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output: Path(a.output).write_text(body,encoding="utf-8")
    else: print(body,end="")

if __name__ == "__main__": main()
