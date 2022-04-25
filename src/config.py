from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE


"""Global variables"""

# content type
IMAGE_KEY: str = "image"
TEXTBOX_KEY: str = "textbox"

# shapes pointing contents
SHAPES = {
    "image": MSO_SHAPE.RECTANGLE,
    "textbox": MSO_SHAPE_TYPE.TEXT_BOX
}

# delimiter (GUI filesbrowse)
FILES_BROWSE_DELIMITER = ";"

# delimiter (label)
DELIMITER: str = "_"

# regex
"""
. : 任意の1文字
\d : 任意の数字

* : 0回以上の繰り返し
+ : 1回以上の繰り返し

^ : 文字列の先頭
$ : 文字列の末尾

() : グループ化

.* : 任意の文字を0回以上繰り返し(あってもなくても良い)
"""
# 画像の拡張子を指すパターン
REGEX_IMAGE = '/*\.(jpg|jpeg|png|bmp)'
# groupを指すパターン : [@1, ＠2, @_1, @ 1...]
REGEX_POINTING_GROUP = '(@|＠).*\d+'
# labelを指すパターン
REGEX_POINTING_LABEL = '(#|＃).*\d+'