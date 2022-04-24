from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE


"""Global variables"""

# contnet type
IMAGE_KEY: str = "image"
TEXTBOX_KEY: str = "textbox"

# shape
SHAPES = {
    "image": MSO_SHAPE.RECTANGLE,
    "textbox": MSO_SHAPE_TYPE.TEXT_BOX
}

# sepalater
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

REGEX_IMAGE = '/*\.(jpg|jpeg|png|bmp)'
# groupを指す文字 : [@1, ＠2, @_1, @ 1...]
REGEX_POINTING_GROUP = '(@|＠).*\d+'
# labelを指す文字
REGEX_POINTING_LABEL = '(#|＃).*\d+'

CORRESPONDING_OLD_NEW_TEXT = {
    REGEX_POINTING_GROUP: "group_id",
    REGEX_POINTING_LABEL: "label",
}