#!/bin/zsh

export SRC_DIR="スクリプトのパス"
export PATH="$HOME/.poetry/bin:$PATH"

cd ${SRC_DIR}
poetry run python main.py
