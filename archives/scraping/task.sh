#!/bin/zsh

export SRC_DIR="/Users/westen/dev/python-automations/scraping"
export PATH="$HOME/.poetry/bin:$PATH"

cd ${SRC_DIR}
poetry run python main.py
