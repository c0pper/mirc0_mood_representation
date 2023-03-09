import streamlit as st
from annotated_text import annotated_text
from pathlib import Path
from classes import Pratica
from visual import colors
import legenda


def get_gap_tuples(lst):
    result = []
    for i in range(len(lst) - 1):
        curr_tuple = lst[i]
        next_tuple = lst[i + 1]
        if curr_tuple[1] + 1 != next_tuple[0]:
            result.append((curr_tuple[1] + 1, next_tuple[0] - 1))

    return result


def get_category_indexes(categorization: list) -> list:
    category_indexes = []
    for category in categorization:
        for rule in category["rules"]:
            for scope in rule["scope"]:
                # print(category["name"], txt[scope["begin"]:scope["end"]])
                # print("begin:", scope["begin"])
                # print("end:", scope["end"])
                category_indexes.append((scope["begin"], scope["end"], category["name"]))
    return sorted(set(category_indexes), key=category_indexes.index)


st.set_page_config(layout="wide")

show_legend = st.sidebar.checkbox("Mostra legenda")

folder_pratica = st.sidebar.selectbox(
    "Seleziona pratica",
    list(Path("pratiche").glob("*"))
)

p = Pratica(folder_pratica)
calls = p.calls

call = st.sidebar.selectbox(
    "Seleziona chiamata",
    list(c.call_id for c in calls)
)

call_obj = [c for c in calls if c.call_id == call]

categorization1 = call_obj[0].speaker1_categorization
txt1 = call_obj[0].speaker1_txt

categorization2 = call_obj[0].speaker2_categorization
txt2 = call_obj[0].speaker2_txt

if show_legend:
    for k, v in legenda.legend.items():
        with st.container():
            k_col, v_col = st.columns(2)

            with k_col:
                st.markdown(k, unsafe_allow_html=False)
            with v_col:
                st.markdown(v, unsafe_allow_html=False)
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.header("Testo speaker1")
        for s in txt1.split("\n"):
            st.markdown(s, unsafe_allow_html=False)

    with col2:
        st.header("Mood speaker1")
        for start, end, name in get_category_indexes(categorization1):
            annotated_text((txt1[start:end + 1], name, colors[name]))
            st.text("")


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.header("Testo speaker2")
        for s in txt2.split("\n"):
            st.markdown(s, unsafe_allow_html=False)

    with col2:
        st.header("Mood speaker2")
        for start, end, name in get_category_indexes(categorization2):
            annotated_text((txt2[start:end + 1], name, colors[name]))
            st.text("")
