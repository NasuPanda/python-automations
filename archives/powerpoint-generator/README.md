# パワポ画像貼り付けツール

① PowerPointで作成したフォーマットの位置に画像を出力 ②テキストをデータ名/ラベル名に置換出来るGUIツールです。

![demo-gif](./samples/デモ/PowerPointFormatter_特定レイアウト_デモ.gif)

## 概要

PowerPointで作成したフォーマットを使用して画像貼り付け・テキスト置換を行います。

- 1データに画像が複数存在する場合、指定したラベル位置に画像を貼り付ける事ができます。
  - 1データに対して複数のレイアウト(正面から、上から、、、)の画像が存在するイメージです。
- 連番になっているデータの場合、順番に画像を貼り付ける事ができます。

**主な機能**

- 四角形 → 画像 への置換
  - 四角形の配置 = 画像の配置
  - 四角形のテキスト = 画像のラベル
  - 画像はデータ名とラベルを「 _ 」で区切る
- テキストの置換
  - @1 (@ + 数字) = データ名へ置換
  - #1 (# + 数字) = ラベルへ置換

## 動作環境

アプリケーションを動作させるために以下の環境が必要です。

- Python 3.10.2
- python-pptx 0.6.21
- PySimpleGUI 4.59.0

## 使用方法

### 1データに複数画像が存在する場合(ラベル位置への貼付け)

1データに画像が複数存在する場合、ラベルの位置を指定することで画像を配置します。

**入力フォーマット**

ラベルを指定します。

- 1枚のスライドに1グループの場合は「ラベル名」のみ指定します。
- 1枚のスライドに複数グループが存在する場合、`_` で「連番」と「ラベル名」を区切って指定します。
- PowerPointで指定するラベル名と画像のラベル名は一致させる必要があります。

下の例では 2データ/1スライド なので、「1_右」, 「2_右」のように `_` で「連番」と「ラベル名」を区切ります。
![ラベリング_フォーマット](https://user-images.githubusercontent.com/85564407/165007818-aa214818-b1c2-4a6d-a8a8-8195f7458766.png)

**入力画像**

ねずみ_右の場合は「ねずみ」がデータ名 /「右」がラベルとして扱われます。
![image](https://user-images.githubusercontent.com/85564407/165009884-babf36f4-3558-493b-ad4e-54f3cec36d40.png)

**出力されるPowerPoint**

1枚目
![ラベリング 出力_1](https://user-images.githubusercontent.com/85564407/165007834-7e7db6df-e4a0-432d-ab74-d615ac6f2e33.png)
2枚目
![ラベリング 出力 2](https://user-images.githubusercontent.com/85564407/165009914-4737f8af-1c0d-4c4a-a169-a5156a229505.png)

### 1データに画像が1枚の場合(連番貼り付け)

連番になっているデータの場合、スライドを跨いで順番に画像を貼り付ける事ができます。

**入力フォーマット**

四角形の中に数字を指定します。
![順に貼り付け_フォーマット](https://user-images.githubusercontent.com/85564407/165007744-6061d6e1-22b3-46e7-9d18-9f0f1b865cd8.png)

**入力画像**

fruits_1の場合は「fruits」がデータ名、「1」がラベル(連番)として扱われます。
![image](https://user-images.githubusercontent.com/85564407/165010477-72faaf06-943e-4dda-9170-b9bcca155da9.png)

**出力されるPowerPoint**

連番は0埋めの有無に関係なく、数値の大小で判定されます。

1枚目
![順に貼り付け_出力 1](https://user-images.githubusercontent.com/85564407/165007794-211c05cf-76d9-4563-9d48-42d91bb12728.png)
2枚目
![順に貼り付け_出力 2](https://user-images.githubusercontent.com/85564407/165010628-b2cc1a2c-2767-4cdc-ac12-31311f456887.png)

### GUIの操作

![image](https://user-images.githubusercontent.com/85564407/165257836-e0651fb7-fc15-401c-8996-34e1e3f443cd.png)

#### フォーマットのレイアウトパターンを選択

ラベル位置への貼付け(1画像:複数データ) or 順に並べる(1画像:1データの連番データ)を選択してください。

![フォーマットパターン選択](https://user-images.githubusercontent.com/85564407/165257925-2ef1c50d-1aa1-4860-a57c-99c2c2c1d27e.png)

#### 設定用(フォーマットを作成した)PowerPointの入力

入力前
![入力前](https://user-images.githubusercontent.com/85564407/165258183-e9ec10a5-8492-4bf9-95d6-0547cdb7e735.png)

入力後
![入力後](https://user-images.githubusercontent.com/85564407/165258364-e8dbb38c-f3ee-45dc-bbb6-f4e3546c6440.png)

#### 画像の入力方法を選択・画像ファイルを入力

まず画像の入力方法を選択してください。

##### フォルダ選択

フォルダ選択では選択したフォルダ配下の画像が入力画像になります。

![フォルダ選択](https://user-images.githubusercontent.com/85564407/165258498-f4b888d0-a8e4-4d25-87e5-c17e05c50d52.png)

##### ファイル選択

ファイル選択では選択したファイルが直接入力画像になります。

![ファイル選択](https://user-images.githubusercontent.com/85564407/165258555-3d9d3254-dcab-49a4-aceb-b3705fa8402e.png)

右下から拡張子の選択が可能です。(Windowsの場合)

![拡張子の選択](https://user-images.githubusercontent.com/85564407/165258701-41de7008-8700-4431-9ab8-554ad972c6a4.png)

![ラベル箇所の選択](https://user-images.githubusercontent.com/85564407/165258853-f54c199f-aa63-4389-a1bf-fadf908cba17.png)

##### レイアウト(ラベル) or 連番 部分の選択

画像ファイル名を `_` で区切った単語が表示されます。
レイアウト(ラベル) or 連番に当たる箇所を選択してください。

#### 出力ファイル名の入力・処理の実行

出力ファイル名を入力してください。

何も入力しなかった場合は自動的に現在時刻が割り当てられます。

「出力ファイルを開く」にチェックを入れると処理が終了した時に出力されたファイルを自動的に開きます。

![入力しなかった場合](https://user-images.githubusercontent.com/85564407/165259219-db480535-f07b-4ec4-8ea8-a0cc7b403b2e.png)

デフォルトでは`main.py`と同じフォルダに出力されます。

## 動作サンプルに使用した画像

- [【フリーアイコン】 フルーツ](https://sozai.cman.jp/icon/food/fruits/)
- [【フリーアイコン】 矢印（上下左右）](https://sozai.cman.jp/icon/arrow/base1/)