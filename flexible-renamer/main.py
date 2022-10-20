from src.models.file import FileFilter, FileRenamer
from src.views.presentational import components

new_names = ["A", "b", "c", "d", "e"]
layouts = ["上", "下"]


for layout in layouts:
    filter = FileFilter(src_folder="./samples/")
    filter.filter_by_extension(".txt")
    filter.filter_by_include(layout)

    renamer = FileRenamer(src_files=filter.paths)
    renamer.replace_parts(new_names, 1)
    renamer.swap_parts(0, 1)
    renamer.copy_from_src_to_dst("./test")
