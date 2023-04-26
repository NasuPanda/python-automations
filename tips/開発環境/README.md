# 快適なPython開発環境構築の覚書
## 導入すると良いもの

- pipenv または poertry ... パッケージ管理.
- black ... コードフォーマッタ.
- flake8 ... リンター.
- isort ... import文をキレイにする.
- mypy ... 型.
- ipython ... パスやライブラリの補完が効いたり、履歴をファイルに出力できたり. 便利な対話型インターフェース.

### 補足
#### パッケージ管理ツール
プロジェクトごとのパッケージ管理や仮想環境構築を簡単に、自動でやってくれるツール.

- [Pipenvを使ったPython開発まとめ - Qiita](https://qiita.com/y-tsutsu/items/54c10e0b2c6b565c887a)
- [Poetryをサクッと使い始めてみる - Qiita](https://qiita.com/ksato9700/items/b893cf1db83605898d8a)

#### コーディング規約の遵守
PythonにはPEP8というコーディング規約がある.
皆が自由にコードを書くとぐちゃぐちゃになってしまうので、「これを参考にしてわかりやすいコードを書こうね」というもの.

できる限りPEP8を遵守したコードを書いた方が「他の開発者にとって良いコードが書ける」と言って差し支えない.

とはいえ、スペースや改行の数、インデント具合など本質的でない箇所に時間を取られるのはいただけない.

そこで登場するのが black などのツール. 「ルールに従ったコードに整形する」などという作業はツールに任せれば良いという考え方である.

### 手順
手順は[VSCodeでPython書いてる人はとりあえずこれやっとけ〜 - Qiita](https://qiita.com/nanato12/items/ddf26487eb30714251c3)を参照.
基本的には `pip install [パッケージ]` して VSCode の保存時に自動的に実行されるように設定するだけ.

上記記事に加えてipythonを導入しておけばOK.

### 参考
- [VSCodeでPython書いてる人はとりあえずこれやっとけ〜 - Qiita](https://qiita.com/nanato12/items/ddf26487eb30714251c3)
- [black](https://github.com/psf/black)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [isort](https://flake8.pycqa.org/en/latest/)
- IPython
  - [Jupyter and the future of IPython — IPython](https://ipython.org/)
  - [IPythonの使い方 - Qiita](https://qiita.com/5t111111/items/7852e13ace6de288042f)

---

## その他
### VSCode > `settings.json`

Pythonのキャッシュや仮想環境関連のフォルダなどは検索対象から外しておくと良い。

```json
{
    "files.exclude": {
        "**/.mypy_cache/**": true,
        "**/__pycache__/**": true,
        "**/.pytest_cache/**": true,
    },
    // 監視しないファイル名/ディレクトリ名のパターン
    "files.watcherExclude": {
        "**/.git/objects/**": true,
        "**/node_modules/**": true,
        "**/vendor/**": true,
        "**.mypy_cache/**": true,
        "**/.venv/**": true,
    },
    // 検索対象から外すファイル・ディレクトリのパスのパターン
    "search.exclude": {
        "**/node_modules": true,
        "**/bundle": true,
        "**/tmp": true,
        "**/.tmp": true,
        "**.mypy_cache/**": true,
        "**/.venv/**": true,
    },
    // ︙
    "[python]": {
        "editor.tabSize": 4,
        "editor.insertSpaces": true,
        "editor.formatOnSave": true,
        "editor.formatOnPaste": true,
        "editor.codeActionsOnSave": {
            // isort
            "source.organizeImports": true,
        },
        "editor.formatOnType": true,
    },
}
```

### .gitignore

Python用の `.gitignore` を用意しておいて使い回すと楽。

```.gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/
```
