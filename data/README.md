# Dataset

Place `Feature_Extraction_v12_1000balanced.jsonl` in this directory.

Expected path in this repository:

```text
data/Feature_Extraction_v12_1000balanced.jsonl
```

The loader in `src/load_feature_data.py` can read either:

- a local file path
- a GitHub raw URL
- a gzip-compressed `.jsonl.gz` file

After the dataset is uploaded, the raw URL will be:

```text
https://raw.githubusercontent.com/hsun0912/5703sunhao/main/data/Feature_Extraction_v12_1000balanced.jsonl
```
