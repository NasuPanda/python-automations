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

***

# Beautiful Soup

## 参考

- [10分で理解する Beautiful Soup - Qiita](https://qiita.com/Chanmoro/items/db51658b073acddea4ac)
  - 基本的な使い方から実践的なテクニックまで、さっくりまとまっている

## 使い方

### `select`

CSSセレクタを書いてタグを取得出来る。
返り値は `ResultSet[Tag]` であり、コレクション型。

### テキスト検索

Beautiful Soup は関係なく一般的なCSSセレクターの書き方の話になるが、 `:soup-contains` を使うと指定したテキストを含む要素が取得出来る。

```py
soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
results = soup.select("h4:-soup-contains('ワンパンマン')")
```

### 親階層のノードにアクセス

`Tag` インスタンスの `.parent` プロパティにアクセスする。

### 同じ階層の隣接ノードにアクセス

`~` を使う。

```py
tag_items = soup.select('h2:contains("Top Ten tags") ~ span')
print([t.get_text(strip=True) for t in tag_items])
# > ['love', 'inspirational', 'life', 'humor', 'books', 'reading', 'friendship', 'friends', 'truth', 'simile']
```

# Selenium

## webdriver-managerを使う

ドライバーの管理を自動化出来るライブラリ。

```py
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url = "https://tonarinoyj.jp/series"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
```

ヘッドレスの場合も変わらず。

```py
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://www.example.com/")
```

## 使い方

Selenium で要素を取得する場合、大抵操作を目的としている。

### `find_**`

`find_**` 系のメソッドで条件に合致する要素を取得出来る。

```py
elements = driver.find_elements("css selector", ".series-table-list")
pprint.pprint(elements)
```

### URLを開く

`get` を使う。
URLを使って直接ページ遷移したい時も同様。

```py
driver.get(url)
```
