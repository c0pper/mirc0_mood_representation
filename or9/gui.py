from nicegui import ui
import pandas as pd
from or9 import get_pratiche_from_excel



df = pd.read_excel("tags_da_taggatori_dic_gen.xlsx")
pratiche = get_pratiche_from_excel(df)

with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    ui.label(f"").style('color: #FFFFFF; font-size: 200%; font-weight: 300')
    ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=menu')

with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #000000') as left_drawer:
    ui.label('Pratiche')

    for p in pratiche:
        with ui.expansion(p.id_pratica, icon='folder').classes('w-full bg-gray-800'):
            for c in p.calls:
                ui.link(f"+ {c.id_chiamata}\n", f'/{p.id_pratica}/{c.id_chiamata}')

ui.run()