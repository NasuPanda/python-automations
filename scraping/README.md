# スクレイピング

## 環境

- MacOS Monterey 12.5
- python = 3.9.0
- poetry 1.1.14

```ini
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.1"
bs4 = "^0.0.1"
selenium = "^4.3.0"
webdriver-manager = "^3.8.3"
```

## スクレイピングとは

> 英語のスクレイプ（scrape）には、「こすり落とす」「削り取る」という意味があります。スクレイピングとは、Webサイトから公開されているデータを収集し1、そのデータから不要なデータを削り取り、実行者の意図した情報を抜き出す作業を指します。我々は通常、ブラウザーを使って、Webサービスの提供者が意図したテキストとデザインのページを閲覧します。一方、スクレイピングでは、実行者が意図した情報が得られるように、プログラムを使ってWebサービスの情報を抽出します。
>
> 引用 : スクレイピング・ハッキング・ラボ　Pythonで自動化する未来型生活 (Japanese Edition) (p.10). Kindle 版.

## Pythonにおけるスクレイピング

よく使うライブラリ

- Beautiful Soup
  - HTMLを要素単位で解析するパーサ
- requests
  - HTTP / HTTPS 通信によりWebページからHTMLを取得
- selenium
  - 複雑な操作を必要とするページヘのアクセスに
  - 直リクエストに対して `403 forbidden nginx` を返してくるサイトに対して、普通にアクセスしたい時に
- webdriver_manager
  - selenium を使うためにはブラウザのバージョンに対応したドライバが必要。その管理を自動化してくれるライブラリ。
