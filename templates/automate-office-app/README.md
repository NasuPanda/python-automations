# Automate Office App
オフィスアプリ自動化のサンプル

- [Automate Office App](#automate-office-app)
  - [Excel](#excel)
    - [必要なパッケージ](#必要なパッケージ)
    - [使い方](#使い方)
  - [PowerPoint](#powerpoint)
    - [必要なパッケージ](#必要なパッケージ-1)
    - [使い方](#使い方-1)

## Excel
### 必要なパッケージ
[openpyxl](https://openpyxl.readthedocs.io/en/stable/)

```
pip install openpyxl
# or
pip install -r requirements.txt
# or
pipenv install
```

### 使い方
- 基本: `sample_excel.py` を参照
- 画像: `/common/constants.py` を参照
- グラフ: `/excel/accessor.py` 及び `/excel/types.py` を参照
  - FIXME: 汎用性無

## PowerPoint
### 必要なパッケージ
[python-pptx](https://python-pptx.readthedocs.io/en/latest/index.html)

```
pip install python-pptx
# or
pip install -r requirements.txt
# or
pipenv install
```

### 使い方
- 基本: `sample_ppt.py` を参照
- 詳細、機能の追加: `/ppt/types.py` 及び `/ppt/accessor.py` を参照・編集
