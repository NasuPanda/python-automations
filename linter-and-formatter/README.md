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

