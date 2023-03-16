from nicegui import ui
from pathlib import Path


with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    ui.label('HEADER')
    ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=menu')
with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #d7e3f4') as left_drawer:
    ui.label('LEFT DRAWER')

ui.label('CONTENT')
[ui.label(f'Line {i}') for i in range(100)]

ui.run()