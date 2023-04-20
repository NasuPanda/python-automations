import PySimpleGUI as sg
import pptx
from typing import TypedDict

class Content(TypedDict):
    coordinates: tuple[int, int]
    size: tuple[int, int]
    label: str


content: Content = {"coordinates": (10, 10), "size": (100, 100), "label": "ID"}
print(content)
a = input("コレが出たらOK")