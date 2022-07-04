# .parファイル解析ツール

.par([VersaStudio](https://www.ameteksi.jp/products/software/versastudio-software-jp)製ソフトから出力される試験結果ファイル)ファイルの解析ツール。

## 概要

1. .parファイルをCSVファイルへ変換
2. CSVファイルから必要なデータを抜き取る
3. データをもとに算出したとある値をGUIに表示、ユーザに値を調節してもらう
4. Excelにデータ, グラフ(散布図)を出力

## 環境

- Python 3.10.2
- openpyxl
- pandas
- PySimpleGUI
- pywin32
- pypwin32
- scipt

## 実装・注意点

- MVCアーキテクチャを採用しています。
- GUIにはPySimpleGUIというライブラリ(tkinterのラッパー)を使用しています。
  - 公式: https://pysimplegui.readthedocs.io/en/latest/call%20reference/
- Pythonのバージョンは多少低くても問題ありませんが、TypedDict(型定義出来る辞書)を使用しているためTypedDict導入以前のバージョンを使用していると問題があるかもしれません。その場合は型定義を外す、あるいは公式ドキュメントを参照してTypedDictを導入してもらえば問題ないと思います。
- 一部クラス(VIData等)で `@dataclass` を使用しています。構造体のようなクラスを定義するためのものです。

### `.par`ファイルの形式

※ 2022年7月時点での仕様

想定しているのはASCIIフォーマットの`.par`ファイルです。

参考 : [公式仕様書](https://www.ameteksi.jp/-/media/ameteksi/download_links/documentations/supportcenter/princetonappliedresearch/productmanuals/versastudio-manual.pdf?revision=0988628f-b3bd-4748-bfad-b3df1d5e4482#page=95) の**Save New Data to Binary File**欄

ASCIIフォーマットの場合、対象とするデータが存在するのは`<Segment1> ~ </Segment1>`になります。

```.par
.
.
.
<Segment1>
Type=2
Version=3
Definition=Segment #, Point #, E(V), I(A), Elapsed Time(s), ADC Sync Input(V), Current Range, Status, E Applied(V), Frequency(Hz), E Real, E Imag, I Real, I Imag, Z Real, Z Imag, E2 Status, E2(V), E2 Real, E2 Imag, Z2 Real, Z2 Imag, ActionId, AC Amplitude, 0
0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
0,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0
.
.
.
```