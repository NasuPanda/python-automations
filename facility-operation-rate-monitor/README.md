# 稼働監視

## 要件

MUST
- PC使用設備の稼働時間が自動で収集できること
- 工数（人がかかわる時間）の収集（マウス動作などを検出・・・他）
  - マウス操作及びキー入力があれば稼働, 一定時間無ければ非稼働として記録すること
  - 非稼働判定とする経過時間の指定ができること
- スタンドアローンで動作すること
- 設備使用者にソフトを作動させずに収集できること（収集忘れを防止）
- 実行形式のソフトで、簡単に導入できること
- 定期的にUSBなどでデータが引き出せ、表計算ソフトなどで集計できること
- 導入～データ引き出し、集計の手順書作成

WANT
- プログラム動作など工数以外の設備作動時間の収集
  - マウス操作中(= 人間が何らかの操作をしている時)
  - 設備稼働中
- Windowsのバージョンに関係なく動作すること

### ファイルとしてログを吐き出す

- ネットワークに繋げない設備が対象のため、ローカルでデータを永続化出来ること
  - 形式はCSV。
- Cドライブ直下辺りにログ用のディレクトリを作成し、そのディレクトリを利用する
  - もしくは、ログ解析用のダッシュボード的なクライアントアプリを作成, ユーザのPC上でCSVログを読み込んで結果を確認出来るようにする。
- ファイル名に設備名とタイムスタンプを含むこと
  - 設備名は設定出来るようにする。
  - 202204041-20220430_設備A_稼働率.csv のように期間がわかるようにする。
- ファイルが存在しなければ作成, 存在すれば既存のファイルに追加していくこと

### 稼働/非稼働の判定

- 実工数(人間が作業している時間)
- マシンタイム(設備のみが稼働している時間)

を切り分けたい。

#### 実工数

マウス及びキーボード入力があった時 = 実工数とする。

#### マシンタイム

特定の設備が稼働する際、基本的には制御ソフトのCPU負荷が上昇する。
そこで、特定のプロセスを監視、CPU負荷が一定以上の場合はマシンタイムとする。

なお、マウス及びキーボード入力有り かつ CPU負荷一定以上 の場合は実工数とする(=**実工数が優先される**)。

### 自動起動

Windowsロック・アンロック時やログオン・ログオフ時に実行されるタスクを登録すれば良い。

## 使用ライブラリ

- arrow
  - https://arrow.readthedocs.io/en/latest/#example-usage
  - Arrow is a Python library that offers a sensible and human-friendly approach to creating, manipulating, formatting and converting dates, times and timestamps.
- pynput
  - https://pynput.readthedocs.io/en/latest/
  - This library allows you to control and monitor input devices.
- psutil
  - https://psutil.readthedocs.io/en/latest/
  - psutil (python system and process utilities) is a cross-platform library for retrieving information on running processes and system utilization (CPU, memory, disks, network, sensors) in Python.
- ruamel.yaml
  - https://yaml.readthedocs.io/en/latest/
  - ruamel vs PyYAML
    - In this case, ruamel is superior for some reasons.
    - PyYAML needs option to handle Japanese(unicode). ruamel is allow unicode by default.
    - PyYAML doesn't maintain data order. ruamel maintain order.

---
メモ
---

## pynput

### `join`メソッド

- threading: https://docs.python.org/ja/3/library/threading.html#threading.Thread.join
- pynput: https://pynput.readthedocs.io/en/latest/private.html?highlight=join#pynput._util.AbstractListener.join

> スレッドが終了するまで待機します。
> このメソッドは、 join() を呼ばれたスレッドが正常終了あるいは処理されない例外によって終了するか、オプションのタイムアウトが発生するまで、メソッドの呼び出し元のスレッドをブロックします。

- joinが呼ばれたスレッドが終了するまで待機する。
- joinが呼ばれたスレッドが終了するまで呼び出し元のスレッドをブロックする。
- joinが呼ばれない場合、次の処理に移ってしまう = 先にメインスレッドが終了してしまう。

## psutil

- PySimpleGUIのCPU監視GUIサンプル
  - これは想定している形式ではない
  - https://github.com/PySimpleGUI/PySimpleGUI-Rainmeter-CPU-Cores/blob/master/PySimpleGUI_Rainmeter_CPU_Cores.py
- How to get current cpu & ram usage
  - https://stackoverflow.com/questions/276052/how-to-get-current-cpu-and-ram-usage-in-python
- Monitoring Python process
  - `psutil.Process()`を引数無しで呼び出すと現在のプロセス=実行中の`**.py`が対象になる
- https://www.thepythoncode.com/article/make-process-monitor-python

### プログラム上のプロセスと実プロセスの乖離を防ぐ

特定プロセスを監視する機能が欲しいため、監視対象は指定できる必要がある。
`pid`(各プロセス固有のID)はランダムなので、名前でプロセスを探すようにする。

名前で指定する場合の問題点は、プログラム上でプロセスを指すオブジェクト(ここでは`Process`クラスとする)と実際のプロセスが乖離する可能性があること。

1. プロセス1が起動している。
   1. 名前でプロセスを探索。
   2. 発見。`Process`のインスタンスを生成。
2. プロセス1が再起動された。
   1. 名前でプロセスを探索。
   2. 発見。`Process`のインスタンスはそのまま。

そのため、`pid`が異なる場合やプロセスが実際には停止している場合にもプロセスを指すオブジェクトを更新する必要がある。

### 監視時の負荷

常時監視の場合、自身のPCだと12~13%程度上昇した。
`sleep`を適宜挟むようにすれば5%前後。


### `cpu_percent`

https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent

```py
import psutil
# blocking
psutil.cpu_percent(interval=1) # => 2.0

# non-blocking (percentage since last call)
psutil.cpu_percent(interval=None) # => 2.9

# blocking, per-cpu
psutil.cpu_percent(interval=1, percpu=True) # => [2.0, 1.0]
```

NOTE: 監視間隔に注意

メソッド呼び出し感覚が短すぎると必ず0.0を返す。
必ずCPU関連のメソッド単体で呼び出すか、呼び出し前に待つようにする。

```py
print(proc.cpu_usage(1))
print(proc.name())

# => 3.1
# => Taskmgr.exe

print(proc.name())
print(proc.cpu_usage(1))

# => Taskmgr.exe
# => 0.0
```

### `Process`

https://psutil.readthedocs.io/en/latest/#process-class

`Process`クラスは各プロセスを表すクラス。
インスタンスの初期化には`pid`を使う。

### `memory_info`

https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_info

## ログ(CSV)

### Excelで開いたときに文字化けする

`utf8`指定だとExcelで開いた際に文字化けする。
`utf_8_sig`を指定する。

```py
with open(self.log_filepath, "a", encoding="utf_8_sig", newline="") as f:
    writer = csv.DictWriter(f, self.headers)
    writer.writerow(log.data_row_as_dict)
```

## 自動起動 ( Windows前提 )

- コマンドで登録 : [schtasksコマンドでWindowsのタスクスケジューラに特権が必要なタスクを登録する - Qiita](https://qiita.com/minamijoyo/items/8cdb1b3659c703f60969)
  - 日本語文字化け問題 : [UTF-8のバッチファイルが文字化けする時の対処3選 – なゆたり](https://nayutari.com/batch-utf8)
- [スクリプトを使ってWindowsのロック・アンロック時に実行するタスクを登録する - Qiita](https://qiita.com/aikige/items/140c51ec87a1b67996b6)
- [homeBinWin/setup at master · aikige/homeBinWin](https://github.com/aikige/homeBinWin/tree/master/setup)
- https://stackoverflow.com/questions/26160900/is-there-a-way-to-add-a-task-to-the-windows-task-scheduler-via-python-3

### タスクスケジューラを扱う

トリガー等の指定には定数を使う。~~わかりにくい~~

- 例: https://docs.microsoft.com/ja-jp/windows/win32/taskschd/daily-trigger-example--scripting-
- 定数について: https://docs.microsoft.com/ja-jp/windows/win32/api/taskschd/#enumerations
- `scheduler.NewTask`の返り値: https://docs.microsoft.com/ja-jp/windows/win32/taskschd/taskfolder-registertaskdefinition
- TaskPriority: https://docs.microsoft.com/ja-jp/windows/win32/taskschd/tasksettings-priority
  - 詳細: https://docs.microsoft.com/ja-JP/windows/win32/procthread/scheduling-priorities

```py
import win32com.client


TASK_SCHEDULE_SERVICE = "Schedule.Service"
TASK_TRIGGER_SESSION_STATE_CHANGE = 11
TASK_ACTION_EXEC = 0
TASK_CREATE_OR_UPDATE = 6
TASK_LOGON_NONE = 0
NO_USER = ""
NO_PASSWORD = ""

TASK_SESSION_LOCK = 7
TASK_SESSION_UNLOCK = 8

scheduler = win32com.client.Dispatch(TASK_SCHEDULE_SERVICE)
scheduler.Connect()

def register_task(scheduler, state_change, name, command):
    folder = scheduler.GetFolder("\\")

    definition = scheduler.NewTask(0)

    trigger = definition.Triggers.Create(TASK_TRIGGER_SESSION_STATE_CHANGE)
    trigger.StateChange = state_change

    action = definition.Actions.Create(TASK_ACTION_EXEC)
    action.Path = command
    # 引数をセットしたい場合
    # action.Arguments = arguments

    folder.RegisterTaskDefinition(
        name,
        definition,
        TASK_CREATE_OR_UPDATE,
        NO_USER,
        NO_PASSWORD,
        TASK_LOGON_NONE
    )

register_task(
    scheduler=scheduler,
    state_change=TASK_SESSION_LOCK,
    name="When Lock",
    command=lock_command
)
```

例えば`python foo.py`を実行したいなら、`command`(`action.Path`)に`python.exe`のパスを指定し、引数`arguments`(`action.Arguments`)に`foo.py`のパスを指定する。

### win32clientのデバッグ

win32clientは以下のような例外しか出ず、そのままだとよくわからない。

```py
(-2147352567, '例外が発生しました。', (0, None, None, None, 0, -2147024891), None)
```

`win32api.FormatMessage`を使うとエラーメッセージを確認出来る。

```py
import win32api

win32api.FormatMessage(-2147024891)
# => 'アクセスが拒否されました。\r\n'
```

## Windows

### バッチファイルのデバッグ

Windowsバッチファイルで何らかのスクリプトを実行した場合、実行終了時にすぐにウィンドウが閉じてしまい、結果がよくわからない。

実行後に止めたい場合は`pause`を使う。

```bat
pause
```

### `.vbs`によりバッチファイルを非表示に

以下のようなスクリプトを使うことでバッチファイルを非表示にすることが出来る。

```vb
Set ws = CreateObject("Wscript.Shell")
ws.run "cmd /c exec.bat", vbhide
```

### `@echo off`

`echo off`は余計な出力を抑制するためのコマンド。
だが、そのままだと`echo off`コマンド自体が表示されてしまう。

そこで、コマンドの先頭に`@`を付ける。
`@`を付けるとバッチファイル中で実行コマンドを表示しないので、`echo off`自体を非表示にすることが出来る。

### `prompt $`

`prompt $`を使うと、カレントディレクトリの場所を表示しないように出来る。

```bat
rem 表示を消す
prompt $

rem 表示を元に戻す
prompt $p$g
```

### `color`

`color`を使うとコマンドプロンプトの文字色・背景色を変更できる。
`color 背景 文字`の順。

使える色は以下。

```bat
color ?

色属性は、2 桁の 16 進数で指定します。
1 桁目は背景に、2 桁目は前景に対応します。
各桁には、次のいずれかの値を指定することができます:
    0 = 黒          8 = 灰色
    1 = 青          9 = 明るい青
    2 = 緑          A = 明るい緑
    3 = 水色        B = 明るい水色
    4 = 赤          C = 明るい赤
    5 = 紫          D = 明るい紫
    6 = 黄色        E = 明るい黄色
    7 = 白          F = 輝く白
```
