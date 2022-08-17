import os

from libs.db import creator

DATABASE_PATH = os.path.abspath("./db/DATA.db")

creator.create_shosetsu_table(DATABASE_PATH)
creator.create_tonarinoyj_table(DATABASE_PATH)
creator.create_jumpplus_table(DATABASE_PATH)
