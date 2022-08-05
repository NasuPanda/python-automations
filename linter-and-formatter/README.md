# Pythonのlinter / formatter

## black

コードフォーマッタ。

```shell
# インストール
pip install black

# 整形の実行
black [ファイル名]
```

### VSCodeにおける設定

`which black` (Winなら `where` ) を実行、 `black` のパスを調べる。

1. VSCodeの設定で black を検索。
2. Black Path に 調べたパスを入力
3. Black Args に 任意の設定を追加 : `--line-length=119` など
4. Python › Formatting: Provider を検索、 black を選択する

ここまで来たら、右クリック → ドキュメントのフォーマット (or Shift + Alt + F)で black による整形を実行出来る。

※ Editor: Default Formatter により規定のフォーマッタが設定されているとそちらが優先されてしまうため `null` にしておく。

format on save を `true` にしておけば、保存時にフォーマッタが走るようになる。


## flake8

Pythonのリンター。

```shell
# インストール
pip install flake8

# チェック
flake8 [ファイル名]
```

### VSCodeにおける設定

- `which flake8` (Winなら `where` ) を実行、 `flake8` のパスを調べる。
- flake8 はあくまでリンターなので、警告レベルに留めておくべき。

1. flake8 path と検索し、調べたパスを入力
2. flake8 と検索し、 Python › Linting › Flake8 Category Severity E/F/W を全て warning にする
3. flake8 Args に任意の設定を追加 : max-line-length, ignore(無視するルール), etc...
