# 5703sunhao

Feature extraction dataset and helper code for the Meta-Uncertainty Gate notebook.

## Read the dataset in Colab

After `data/Feature_Extraction_v12_1000balanced.jsonl` is uploaded to this repository, use either of the following options.

### Option A: download from GitHub raw URL

```python
import urllib.request

FEATURES_URL = "https://raw.githubusercontent.com/hsun0912/5703sunhao/main/data/Feature_Extraction_v12_1000balanced.jsonl"
FEATURES_PATH_NOTEBOOK = "/content/Feature_Extraction_v12_1000balanced.jsonl"

urllib.request.urlretrieve(FEATURES_URL, FEATURES_PATH_NOTEBOOK)
print("Downloaded to", FEATURES_PATH_NOTEBOOK)
```

Then keep the existing notebook line:

```python
records = load_jsonl(FEATURES_PATH_NOTEBOOK)
```

### Option B: use the helper loader

```python
!wget -q -O load_feature_data.py https://raw.githubusercontent.com/hsun0912/5703sunhao/main/src/load_feature_data.py

from load_feature_data import load_jsonl, DEFAULT_GITHUB_RAW_URL
records = load_jsonl(DEFAULT_GITHUB_RAW_URL)
```

This avoids mounting Google Drive for the dataset.
