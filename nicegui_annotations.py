from nicegui import ui
from pathlib import Path
from classes import Pratica
from utils import get_category_indexes, get_labels_value
from matplotlib import pyplot as plt
from visual import colors, quasar_colors
import config
from dataclasses import dataclass




@dataclass
class Navigator:
    pratica_id: str
    call_id: str

navigator = Navigator(0.0, 0.0)

def navigate():
    ui.notify(f'Writing x = {navigator.pratica}, y = {navigator.call} to database')
    return navigator.pratica


ok_to_show = ["e181ef3f-8b69-4114-96f9-adc71ce5ede3", "99861b54-81f7-4b7b-8b5c-8300f28f2fb5",
              "e573dba8-6276-4999-8533-965d901d34c7", "9e0e793e-9610-4cef-bcb9-72d57df98900",
              "17e2d03e-25e6-42e3-bcbe-d5b298d8c12f", "63694915-4e5c-44cd-b632-3355d22f0270",
              "3670cd79-8136-43cc-b47b-dbe72683c237", "9fac6629-f287-40a0-8fef-6f10582d2cdb",
              "d7966d93-30fa-4a86-a9e1-7faeddcdd45b", "c0aff848-e134-4da3-853f-0756cd35fab3",
              "a5d10646-d9fb-4256-9656-5580a21c6793", "3cd3d86f-b37e-4a34-9af6-b1b373e2cda5",
              "7294748d-46d3-4144-bb18-730514f9f3fa", "5ce7d519-5f98-4e40-97a2-41fc78ea955a",
              "e779f163-6de8-48bd-b449-c5cff0cef264", "6cb60b07-b884-412e-a49e-d28b836ea7fe",
              "f3cb0f23-c9cd-4015-95f7-36264953cb4a", "7d68ec1e-d078-401d-8dd7-289a5c8c0cce",
              "8f7d8ee1-aedb-419a-94ed-58d1d5b8667f"]

lista_pratiche = [Pratica(p) for p in list(Path("pratiche").glob("*"))]


with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
    with ui.tabs() as tabs:
        ui.tab('Mood PC', icon='home')
        ui.tab('Testo PC', icon='info')
        ui.tab('Mood Deb', icon='home')
        ui.tab('Testo Deb', icon='info')
        ui.tab('graphs', icon='info')
    ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=menu')
with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #000000') as left_drawer:
    # non riesco a fare in modo che quando cambia la pratica nel dropdown cambiano anche le chiamate
    # folder_pratica = ui.select([p.id_ for p in lista_pratiche], value=[p.id_ for p in lista_pratiche][0], on_change=navigate).bind_value_to(navigator, 'pratica_id')
    #
    # p = Pratica(f"pratiche/{navigator.pratica_id}")
    # calls = p.calls
    #
    # call_id = ui.select(list(c.call_id for c in calls if c.call_id in ok_to_show), value=list(c.call_id for c in calls if c.call_id in ok_to_show)[0],
    #                     on_change=navigate).bind_value_to(navigator, 'call_id')
    #
    #
    # ui.label("").bind_text_from(navigator, "pratica_id")

    ui.label('Pratiche')
    for p in lista_pratiche:
        with ui.expansion(p.id_).classes('w-full'):
            for c in p.calls :
                if c.call_id in ok_to_show:
                    ui.link(c.call_id, f'/{p.id_}/{c.call_id}').props("leading-10")
                    ui.label("")



@ui.page('/{p_id}/{call_id}', dark=True)
def page(p_id: str, call_id: str):
    p = Pratica(Path(f"pratiche/{p_id}"))
    calls = p.calls

    call_obj = [c for c in calls if c.call_id == call_id]

    speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, call_id = get_labels_value(row=0,
                                                                                                   data_list=call_obj)

    categorization1 = call_obj[0].speaker1_categorization
    txt1 = call_obj[0].speaker1_txt

    categorization2 = call_obj[0].speaker2_categorization
    txt2 = call_obj[0].speaker2_txt




    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label(f"{p_id} / {call_id}").style('color: #FFFFFF; font-size: 200%; font-weight: 300')
        with ui.tabs() as tabs:
            ui.tab('graphs', icon='pie_chart_outlined')
            ui.tab('Mood PC', icon='sentiment_satisfied')
            ui.tab('Testo PC', icon='article')
            ui.tab('Mood Deb', icon='sentiment_satisfied')
            ui.tab('Testo Deb', icon='article')
        ui.button(on_click=lambda: left_drawer.toggle()).props('flat color=white icon=menu')
    with ui.left_drawer(top_corner=True, bottom_corner=True).style('background-color: #000000') as left_drawer:
        ui.label('Pratiche')

        for p in lista_pratiche:
            with ui.expansion(p.id_, icon='folder').classes('w-full bg-gray-800'):
                for c in p.calls:
                    if c.call_id in ok_to_show:
                        ui.link(f"+ {c.call_id}\n", f'/{p.id_}/{c.call_id}')
                        ui.label(" ")
                        ui.label(" ")

    frasi_operatore = dict()
    for start, end, name, scope_score in get_category_indexes(categorization1):
        frasi_operatore[txt1[start:end + 1]] = name
    frasi_debitore = dict()
    for start, end, name, scope_score in get_category_indexes(categorization2):
        frasi_debitore[txt2[start:end + 1]] = name

    with ui.tab_panels(tabs, value='graphs'):
        with ui.tab_panel('graphs'):
            with ui.row():
                with ui.column():
                    with ui.pyplot(figsize=(8, 6), facecolor="#1d1d1d"):
                        plt.pie(speaker1_values, labels=speaker1_labels, colors=[colors[v] for v in speaker1_labels],
    autopct='%1.1f%%', textprops={'color':"w"})
                        plt.title("Operatore", color="white")
                with ui.column():
                    with ui.pyplot(figsize=(8, 6), facecolor="#1d1d1d"):
                        plt.pie(speaker2_values, labels=speaker2_labels, colors=[colors[v] for v in speaker2_labels],
    autopct='%1.1f%%', textprops={'color':"w"})
                        plt.title("Debitore", color="white")


        with ui.tab_panel('Mood PC'):
            # for start, end, name, scope_score in get_category_indexes(categorization1):
            #     ui.label(txt1[start:end + 1]).style(config.TRANSCRIPTION_TEXT_STYLE).classes(f'rounded-2xl flex bg-[{colors[name]}] m-2').tooltip(name)
            #     ui.badge(name, color=quasar_colors[name]).classes("text-base")

            for d in call_obj[0].speaker1_domain_objects:
                for rule in d.rules:
                    for scope in rule.scopes:
                        operands_text = list()
                        for op in scope.operands:
                            text = op.get_operand_text(call_obj[0].speaker1_txt)
                            operands_text.append(text)
                        with ui.label(scope.get_scope_text(call_obj[0].speaker1_txt)).style(config.TRANSCRIPTION_TEXT_STYLE).classes(
                            f'rounded-2xl flex bg-[{colors[d.name]}] m-2'):
                            ui.tooltip(" | ".join(o for o in operands_text)).classes("text-lg")
                        ui.badge(f"{d.name}, score: {round(scope.score/d.score, 2)}", color=quasar_colors[d.name]).classes("text-base")


        with ui.tab_panel('Testo PC'):
            for s in txt1.split("\n"):
                if s in frasi_operatore.keys():
                    with ui.label(s).style(config.TRANSCRIPTION_TEXT_STYLE).classes(f'rounded-2xl flex bg-[{colors[frasi_operatore[s]]}] m-2'):
                        ui.tooltip(frasi_operatore[s]).classes("text-lg")
                else:
                    ui.label(s).style(config.TRANSCRIPTION_TEXT_STYLE)

        with ui.tab_panel('Mood Deb'):
            # for start, end, name, scope_score in get_category_indexes(categorization2):
            #     ui.label(txt2[start:end + 1]).style(config.TRANSCRIPTION_TEXT_STYLE).classes(f'rounded-2xl flex bg-[{colors[name]}]/90 m-2').tooltip(f"{name}")
            #     ui.badge(name, color=quasar_colors[name]).classes("text-base")

            for d in call_obj[0].speaker2_domain_objects:
                for rule in d.rules:
                    for scope in rule.scopes:
                        operands_text = list()
                        for op in scope.operands:
                            text = op.get_operand_text(call_obj[0].speaker2_txt)
                            operands_text.append(text)
                        with ui.label(scope.get_scope_text(call_obj[0].speaker2_txt)).style(config.TRANSCRIPTION_TEXT_STYLE).classes(
                            f'rounded-2xl flex bg-[{colors[d.name]}] m-2'):
                            ui.tooltip(" | ".join(o for o in operands_text)).classes("text-lg")
                        ui.badge(f"{d.name}, score: {round(scope.score/d.score, 2)}", color=quasar_colors[d.name]).classes("text-base")


        with ui.tab_panel('Testo Deb'):
            for s in txt2.split("\n"):
                if s in frasi_debitore.keys():
                    with ui.label(s).style(config.TRANSCRIPTION_TEXT_STYLE).classes(f'rounded-2xl flex bg-[{colors[frasi_debitore[s]]}] m-2'):
                        ui.tooltip(frasi_debitore[s]).classes("text-lg")
                else:
                    ui.label(s).style(config.TRANSCRIPTION_TEXT_STYLE)


ui.run()
