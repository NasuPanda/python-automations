# 1スライド/1データ or 1スライド/複数データ
template_slide = Slide()
slides = [Slide() for _ in range(number_of_slide)]
labbeling_images = {"group_id":
    [
        {"path": "", "label": ""},
        {"path2": "", "label": ""},
    ]
}

for slide in slides:
    for _ in range(number_of_group):
        for group_id, images in labbeling_images.items():
            for image in images:
                content = template_slide.search_by_label(image["label"])
                slide.set_content("image", content, group_id)




# 順に並べるデータ
group_id = "引数で受け取るか、image_pathから取り出すか"

slides = [Slide() for _ in range(number_of_slide)]
template_slide = Slide()
# contentsをlabelでソートする (sort に渡す関数を定義すれば出来るはず)
template_slide.sort_contents_by_label()

# image_pathsがソートされていると仮定
image_paths = []
image_index = 0

for slide in slides:
    temp_contents = []
    for i in range(template_slide.get_number_of_contents()):
        content = template_slide.contents["image"][i]
        content.path = image_paths[image_index]
        temp_contents.append(content)
        image_index += 1
    slide.set_contents("image", temp_contents, group_id)