# PythonでExcelのグラフを欠損させずシートをコピーする

## 結論

1. Python (pywin32) により Excel ファイルにシートをコピーするマクロを登録
2. Python (pywin32) からシートをコピーするマクロを実行

```py
# TODO ここにコード
```

## 背景

Python で Excel を操作しようと思った時、真っ先に選択肢に上がるのは [openpyxl](https://openpyxl.readthedocs.io/en/latest/index.html) だと思います。

この openpyxl ですが、シートをコピーした時にグラフが消えてしまいます。

[python - Chart can't be copied with Openpyxl - Stack Overflow](https://stackoverflow.com/questions/67494403/chart-cant-be-copied-with-openpyxl)

業務上、以下のような Excel を扱う機会が多くあるので、それは大変困ります。

- 大量の計算式とその結果を参照するグラフが存在するフォーマット Excel があり、それをコピーして使い回す
- シートごとにグラフが存在する

そこで、どうにか Python だけで **グラフを保持したままシートをコピー出来ないか** 試してみました。

## やったこと

### マクロ実行によるシートのコピー

pywin32 というライブラリを使い、 Excel ファイルに用意しておいたマクロを実行することによりシートをコピーします。
これにより、グラフを保持することが出来ます。

#### pywin32 導入

```shell
pip install pywin32

# pipenv の場合
pipenv install pywin32
```

#### Python からマクロを実行

参考 : [Python – openpyxlでエクセルグラフや図形が消える問題の解決法](https://miya-mitsu.com/python-openpyxl-excel-graph-image-textbox/)

導入するライブラリは pywin32 ですが、使うのは `win32com.client` です。
相対パスだとエラーが出るので絶対パスに変換するようにしています。

```py
import os
import pathlib

import win32com.client

def relative_to_abs(path: str) -> str:
    """相対パスを絶対パスに変換する"""
    return str(pathlib.Path(path).resolve())

src_filename  = relative_to_abs("test.xlsm")
dst_filename = relative_to_abs("result.xlsm")
sheet_name = "sheet1"
macro_name = "CopySheetMacro"

app = win32com.client.Dispatch("Excel.Application")
wb = app.Workbooks.Open(src_filename, ReadOnly=1)
# 非表示にする
app.Visible =  0

sheet = wb.Worksheets(sheet_name).Activate()
app.Application.Run(macro_name)
# VBAの実行でエラーが出ても実行を止めない
app.DisplayAlerts = False

wb.SaveAs(dst_filename)
wb.Close
app.Application.Quit()
```

#### シートをコピーするマクロ

参考 : [VBAでシートをコピーする際のシートの指定方法 ｜ Excel作業をVBAで効率化](https://vbabeginner.net/how-to-specify-a-sheet-when-copying-a-sheet/)

VBA のことはよく分かりませんが、シートの指定方法が3つあるようです。

インデックス指定であれば Python 側との整合性も取りやすい気がするので、インデックス指定を採用しました。

TODO 結果の確認

```vba
Private Sub CopySheet()
    WorkSheets(1).Copy After:=WorkSheets(1)
    ActiveSheet.Name = Format(Now, "YYYY-MM-DD HH.MM.SS")
End Sub
```

### Python によりマクロを登録

マクロがあればコピー出来るとは言っても、フォーマットExcel全てにマクロを搭載するのは面倒です。

同僚に使ってもらおうと思っても、「このマクロを登録してから使ってね！」と言うだけで使用率激減間違いなしです。
そこで、マクロの登録すらも Python から行うことにしました。

TODO コード書く


## 参考

[Python Add Macro to an existing XLSM - Stack Overflow](https://stackoverflow.com/questions/67194521/python-add-macro-to-an-existing-xlsm : PythonからVBAを追加する

[実行時エラー'1004' プログラミングによる Visual Basic プロジェクトのアクセスは信頼性に欠けます のexcel2016での解決方法 - Qiita](https://qiita.com/moitaro/items/03cf067afd5da02b876c) : PythonからVBAマクロを追加出来ない場合

[【Python openpyxlを使用したExcelファイルの読み書き方法】xlsmファイル（マクロありファイル）の場合 - Django Girls and Boys 備忘録](https://kuku81kuku81.hatenablog.com/entry/2022/04/27_python_excel_readwrite_xlsmfile)
