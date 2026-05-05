"""Utilities for loading Feature_Extraction jsonl datasets.

This module supports local paths, GitHub raw URLs, and .gz-compressed jsonl files.
"""

from __future__ import annotations

import gzip
import json
import os
import tempfile
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List

DEFAULT_GITHUB_RAW_URL = (
    "https://raw.githubusercontent.com/hsun0912/5703sunhao/main/"
    "data/Feature_Extraction_v12_1000balanced.jsonl"
)


def _is_url(path_or_url: str) -> bool:
    return path_or_url.startswith(("http://", "https://"))


def download_if_needed(path_or_url: str, cache_dir: str | os.PathLike[str] | None = None) -> Path:
    """Return a local path, downloading URL inputs into a cache directory."""
    if not _is_url(path_or_url):
        return Path(path_or_url)

    cache_root = Path(cache_dir or tempfile.gettempdir()) / "5703sunhao_data"
    cache_root.mkdir(parents=True, exist_ok=True)
    filename = path_or_url.rstrip("/").split("/")[-1]
    local_path = cache_root / filename

    if not local_path.exists() or local_path.stat().st_size == 0:
        print(f"Downloading dataset to {local_path} ...")
        urllib.request.urlretrieve(path_or_url, local_path)

    return local_path


def _open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")


def load_jsonl(path_or_url: str = DEFAULT_GITHUB_RAW_URL, cache_dir: str | os.PathLike[str] | None = None) -> List[Dict[str, Any]]:
    """Load valid records from a Feature_Extraction jsonl file.

    Invalid rows are skipped when they have no `feature_dict` / `features`, have
    `label=None`, or have a label that cannot be converted to int.
    """
    path = download_if_needed(path_or_url, cache_dir=cache_dir)
    records: List[Dict[str, Any]] = []
    skipped = {"malformed": 0, "no_features": 0, "label_none": 0, "label_invalid": 0}

    with _open_text(path) as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                skipped["malformed"] += 1
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                skipped["malformed"] += 1
                continue

            feats = obj.get("feature_dict", obj.get("features"))
            if feats is None:
                skipped["no_features"] += 1
                continue

            raw_label = obj.get("label")
            if raw_label is None:
                skipped["label_none"] += 1
                continue

            try:
                label = int(raw_label)
            except (TypeError, ValueError):
                skipped["label_invalid"] += 1
                continue

            records.append(
                {
                    "features": feats,
                    "label": label,
                    "is_correct": bool(label == 0),
                    "dataset": obj.get("dataset", "unknown"),
                    "sample_id": obj.get("sample_id", f"record_{line_no}"),
                    "task_type": obj.get("task_type", "unknown"),
                    "domain": obj.get("domain", "unknown"),
                    "majority_label_quality": obj.get("majority_label_quality", "unknown"),
                    "prompt": obj.get("prompt", ""),
                    "sampled_answers": obj.get("sampled_answers", []) or [],
                    "is_correct_list": obj.get("is_correct_list", []) or [],
                }
            )

    print(f"Loaded valid records: {len(records)} from {path}")
    print("Skipped:", skipped)
    if not records:
        raise ValueError(f"Loaded 0 valid records from {path_or_url!r}")
    return records


if __name__ == "__main__":
    data = load_jsonl()
    by_label: Dict[int, int] = {}
    for row in data:
        by_label[row["label"]] = by_label.get(row["label"], 0) + 1
    print("Label counts:", by_label)
