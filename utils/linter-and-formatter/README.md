# Pythonのlinter / formatter

## black

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

## isort

`import` の順番を整形してくれる。

```shell
# インストール
pip install isort

# 実行
isort [ファイル名]
```

```python
# 実行前
import mylib
import pathlib
import abc

# 実行後
import abc
import pathlib

import mylib
```
### VSCodeの設定

`which isort` (Winなら `where` ) を実行、 `isort` のパスを調べる。

1. isort と入力、 Python › Sort Imports: Path に調べたパスを入力
2. 以下のように `settings.json` を編集、保存時に自動実行されるようにしておく

```json
{
  // ...
  "editor.codeActionsOnSave": {
    "source.organizeImports": true,
  },
  // ...
}
```

## mypy

Pythonの型チェッカー。

```shell
# インストール
pip install mypy
```

### VSCodeにおける設定

- `which mypy` (Winなら `where` ) を実行、 `mypy` のパスを調べる。
- mypyの型チェックに引っかかったところでエラーが出るわけでも規約違反なわけでも無いので、警告レベルは information にしておく

1. mypy で検索をかけ、PATHを入力
2. Python › Linting: Mypy Enabled を有効に
3. Python › Linting › Mypy Category Severity の Error / Note を information に
4. Python › Linting: Mypy Args に任意の設定を [The mypy command line - mypy 0.971 documentation](https://mypy.readthedocs.io/en/stable/command_line.html) から追加

```json
{
  "python.linting.mypyArgs": [
        "--ignore-missing-imports",
        "--show-column-numbers",
        "--no-pretty",
        "--warn-return-any",
        "--no-implicit-optional",
        "--disallow-untyped-calls",
        "--disallow-untyped-defs",
        "--follow-imports=skip"
    ],
}
```

## 番外: VSCodeの設定

### VSCodeが仮想環境を認識するための条件

公式ドキュメントによると、主に以下の場所にある virtual env を認識する。

1. ワークスペースまたはプロジェクトのディレクトリ直下
2. `python.venvPath` で指定されたディレクトリ以下に配置された virtual env

poetry, pipenv 等の仮想環境を認識して欲しい場合、仮想環境をプロジェクトのディレクトリ直下に作成するような設定をする。
そして、プロジェクトのルートディレクトリをワークスペースとして開く。

### VSCodeでモジュールの補完・解析用のパスを通す

`settings.json` を開き、以下のような設定を追加する。

```json
    "python.analysis.extraPaths": [
        '/Users/usr/dev/foo/.venv/lib/python3.9/site-packages'
    ],
    "python.autoComplete.extraPaths": [
        '/Users/usr/dev/foo/.venv/lib/python3.9/site-packages'
    ]
```
