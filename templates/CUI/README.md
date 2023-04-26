# CLI
## 使用例
![example](./images/スクリーンショット%202023-04-17%20161926.png)

## Spinner
処理待ち用のCLI.

※ 画像だとわかりにくいですがぐるぐるするやつです

![start](./images/スクリーンショット%202023-04-17%20163248.png)
![end](./images/スクリーンショット%202023-04-17%20163316.png)

### 1.` start()` と `stop()` の呼び出し
```python
>> spinner = Spinner(text="Loading...", etxet="Loading... Done.")
>> spinner.start()
>> # Doing something...
>> spinner.stop()
```

### 2. `with`
```python
>> with Spinner("Loading...", "Loading... Done."):
>>     # Doing something...
```

### 3. デコレータ
```python
>> @Spinner("Loading...", "Loading... Done.")
>> def func():
>>     # doing something
>> func()
```
