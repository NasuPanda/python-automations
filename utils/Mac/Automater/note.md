# Pythonスクリプトの自動実行 (Macの場合)

デフォルトだと通っている `PATH` がローカルの環境と異なるので注意。

1. 以下のようなシェルスクリプトを用意 ( poetry の場合 )

  ```zsh
  #!/bin/zsh

  export SRC_DIR="スクリプトのパス"
  export PATH="$HOME/.poetry/bin:$PATH"

  cd ${SRC_DIR}
  poetry run python main.py
  ```

2. Automator > カレンダーアラーム > シェルスクリプトを実行 で以下のようなスクリプトを書く。

  ```bash
  export SRC_DIR="スクリプトのパス"
  source ${SRC_DIR}/task.sh
  ```

3. カレンダーが開くので、イベントを編集する
4. システム環境設定 > バッテリー からタスク実行前にスリープが解除されるように設定しておく
