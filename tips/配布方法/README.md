# Python配布方法

## pyinstaller
Pythonプロジェクトを単一の `.exe` ファイルにするライブラリ.

### auto-py-to-exe
pyinstallerのラッパー. 便利.

[Pythonファイルを超簡単にexeファイル化するGUIソフト - Qiita](https://qiita.com/osorezugoing/items/4ea5249c43c0ba8b89aa)

## Embeddable Python

メリット:
- `.exe`化(pyinstaller等)よりも基本的には軽量。
- 一度環境を用意してしまえば使いまわせるため、楽。
- 仕様変更、機能の追加などによりコードに修正が入った際、ソースコードを置き換えるだけで良い。

### 参考
- [4. Windows で Python を使う — 埋め込み可能なパッケージ](https://docs.python.org/ja/3/using/windows.html#the-embeddable-package)
- [超軽量、超高速な配布用Python「embeddable python」 - Qiita](https://qiita.com/mm_sys/items/1fd3a50a930dac3db299)
- tkinterの導入 : [Python embeddable zip: install Tkinter - Stack Overflow](https://stackoverflow.com/questions/37710205/python-embeddable-zip-install-tkinter)

### 導入の流れ

#### ダウンロード

リンク: https://www.python.org/downloads/release/python-365/

Windows x86-64 embeddable zip file を選択してダウンロード、解凍。
`python-****-embed-win32`以下のファイルはそのままにする。

#### `python**.__pth`ファイルの修正

↓のコメントアウトを解除。

```
# before
# import site

# after
import site
```

#### `get-pip.py`

`python.exe`と同じフォルダに`get-pip.py`を用意する。
ダウンロードするか、以下からコピーしてくる。

https://bootstrap.pypa.io/get-pip.py

#### `**.pth`ファイルを配置

`python.exe`と同じフォルダに`.pth`拡張子のファイルを作成(名前は自由)、以下を追記。

```
import sys; sys.path.append('')
```

#### `pip install`する

コマンドプロンプトで作業する。

```bat
cd "python.exeが居るフォルダ"

# dirでPython.exeが居るフォルダか確認する
dir
# get-pipをインストール
python get-pip.py
```

`python -m pip install`を使って必要なパッケージをインストールする。

ただし、場合によってはフォルダ内のpython.exeではなく自身のPCにインストールしたPythonが呼ばれ、グローバルにインストールされてしまうことがある。

`python.exe -m pip install`の方が安全。

```bat
# インストール
python.exe -m pip install opencv-python

# インストールの確認
python.exe -m pip list
```

### 実行方法

`python.exe`と同じ階層(もしくはユーザに見える上の階層)に、以下のような`.bat`(もしくは `.cmd`)を用意しておく。

`main.bat`を実行すると`main.py`が実行されるだけのもの。

```bat:main.bat
rem このファイルの位置を作業ディレクトリに
cd /d %~dp0

python.exe main.py
```

### 注意点

#### `tkinter`を導入したい場合

1. 組み込みPython(通常のPython)をインストール
   1. https://www.python.org/downloads/release/python-365/ から「embeddable python」 と同じバージョンを選択してインストーラーでインストールすれば良い。
2. https://stackoverflow.com/questions/37710205/python-embeddable-zip-install-tkinter を参考にtkinter関係のフォルダ/ファイルをコピーする

  > 1. tcl folder to embedded_distribution_folder\ (root folder of the embedded distribution)
  > 2. tkinter folder (which is under Lib) either to embedded_distribution_folder\Lib or to embedded_distribution_folder\
  > 3. files _tkinter.pyd tcl86t.dll tk86t.dll (which are under DLLs) either to embedded_distribution_folder\DLLs or to embedded_distribution_folder\
