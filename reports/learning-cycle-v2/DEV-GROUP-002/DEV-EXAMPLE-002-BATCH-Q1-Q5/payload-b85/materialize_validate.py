from __future__ import annotations
import argparse, base64, hashlib, json, zlib
from pathlib import Path


def canonical_bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def object_hash(value):
    body = {k: v for k, v in value.items() if k != "object_hash"}
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--payload-dir", default=str(Path(__file__).parent))
    ap.add_argument("--output", default=str(Path(__file__).parent / "case-batch-artifact-v2.1.json"))
    args = ap.parse_args()
    payload = Path(args.payload_dir)
    manifest = json.loads((payload / "manifest.json").read_text(encoding="utf-8"))
    chunks = []
    for row in manifest["parts"]:
        raw = (payload / row["path"]).read_bytes()
        assert len(raw) == row["bytes"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
        chunks.append(raw.decode("ascii"))
    materialized = zlib.decompress(base64.b85decode("".join(chunks).encode("ascii")))
    assert len(materialized) == manifest["materialized_bytes"]
    assert hashlib.sha256(materialized).hexdigest() == manifest["materialized_sha256"]
    bundle = json.loads(materialized)
    assert bundle["schema"] == "CASE-BATCH-TRAINING-ARTIFACT-V2.1"
    assert bundle["object_hash"] == manifest["bundle_object_hash"]
    assert object_hash(bundle) == bundle["object_hash"]
    assert bundle["batch_completion"]["status"] == "TRAINING_BATCH_COMPLETE_WITH_SENSITIVE_TARGET_EXCLUSION"
    for q in ("Q1", "Q2", "Q3", "Q5"):
        unit = bundle["units"][q]
        reasoning = unit["reasoning_correction"]
        assert len(reasoning["option_semantics"]) == 4
        assert len(reasoning["pairwise_rows"]) == 6
        assert reasoning["contamination_and_answer_memory_audit"]["status"] == "PASS"
        assert reasoning["training_unit_conclusion"]["formal_exact_assertion"] is None
        assert unit["training_unit_completion"]["status"] == "TRAINING_UNIT_COMPLETE"
    excluded = bundle["excluded_units"]["Q4"]
    assert excluded["status"] == "EXCLUDED_UNSCORABLE_SENSITIVE_TARGET"
    assert excluded["accuracy_eligible"] is False
    assert excluded["training_target_eligible"] is False
    assert excluded["formal_exact_assertion"] is None
    Path(args.output).write_bytes(materialized)
    print(json.dumps({"status": "PASS", "output": args.output, "bundle_object_hash": bundle["object_hash"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
