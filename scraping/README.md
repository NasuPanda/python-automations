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
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kinds-of-objects
  - Beautiful Soup のオブジェクトについて

## 使い方

### `select`

CSSセレクタを書いてタグを取得出来る。
返り値は `ResultSet[Tag]` であり、コレクション型。

### テキスト検索

Beautiful Soup は関係なく一般的なCSSセレクターの書き方の話になるが、 `:soup-contains` を使うと指定したテキストを含む要素が取得出来る。

[Pseudo Classes - Soup Sieve](https://facelessuser.github.io/soupsieve/selectors/pseudo-classes/#:-soup-contains)

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

## 参考

- [Selenium webdriverよく使う操作メソッドまとめ - Qiita](https://qiita.com/mochio/items/dc9935ee607895420186#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)
- [Selenium - ページの読み込みが完了するまで待つ(python)](https://codechacha.com/ja/selenium-explicit-implicit-wait/)

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

## URLを開く

`get` を使う。
URLを使って直接ページ遷移したい時も同様。

```py
driver.get(url)
```


## `find_**`

`find_**` 系のメソッドで条件に合致する要素を取得出来る。

```py
elements = driver.find_elements("css selector", ".series-table-list")
pprint.pprint(elements)
```

`selenium.webdriver.common.by.By` を `import` することで使用するか、文字列を直接指定する。

```py
from selenium.webdriver.common.by import By

driver.find_element(By.XPATH, '//button[text()="Some text"]')
driver.find_elements(By.XPATH, '//button')

# 文字列
ID = "id"
NAME = "name"
XPATH = "xpath"
LINK_TEXT = "link text"
PARTIAL_LINK_TEXT = "partial link text"
TAG_NAME = "tag name"
CLASS_NAME = "class name"
CSS_SELECTOR = "css selector"
```

### xpath

親ノードの取得やテキスト検索など、CSSセレクターのみだと面倒な検索も簡単に可能。

```py
# テキスト検索
element = driver.find_element("xpath", f"//h4[text()='{manga_title}']")

# 親ノードの取得
element.find_element("xpath", "../..")

# value で検索
button_login = driver.find_element("xpath", "//input[@value='ログイン']")
```

## プロパティ

### タイトル

```py
driver.title
```

### ページのソース(HTML)の取得

Beautiful Soup にそのまま渡してパースする、など。

```py
driver.page_source
```

### URLの取得

```py
driver.current_url
```
