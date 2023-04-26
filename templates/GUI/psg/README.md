# GUIテンプレ

- [GUIテンプレ](#guiテンプレ)
  - [環境など](#環境など)
  - [詳細](#詳細)
    - [ディレクトリ構造](#ディレクトリ構造)
    - [使い方](#使い方)

![sampleGUI](images/スクリーンショット%202023-04-20%20114715.png)

## 環境など

使用ライブラリ:
- [PySimpleGUI](https://www.pysimplegui.org/en/latest/)
- openpyxl: 動作サンプル用. GUIに必要な訳では無い

環境構築:
```sh
pip install -r requirements.txt
# もしくは
pipenv install
```

## 詳細
### ディレクトリ構造

```
main.py
/gui
  /container          ... UIとロジックをつなぐ
    ui.py             ... UIとロジックをつなぐ
  /presentational     ... UIの見た目のみを定義する
    components.py     ... コンポーネントを定義する
    index.py          ... コンポーネントをまとめて`create_window`関数を定義する
/common
  constants.py        ... 定数の定義
  utils.py            ... 共通して使う処理(極力使わない)
/backend
  /excel              ... Excel操作用
  sample.py           ... 処理のサンプル(設定ファイルを読み込むだけ)
```

### 使い方

1. `/common/constants.py` で定数を定義
2. `/gui/presentational/components.py` でコンポーネントの外見を定義
3. `/backend` で実行したい処理を定義
4. `/gui/container/ui.py` でUI⇔処理のつなぎこみを行う
