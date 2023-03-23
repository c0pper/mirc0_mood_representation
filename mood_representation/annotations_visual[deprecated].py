import streamlit as st
from annotated_text import annotated_text
from pathlib import Path
from classes import Pratica
from visual import colors
from visual import get_labels_value
import plotly.express as px
import legenda
from utils import get_category_indexes


st.set_page_config(layout="wide")

show_legend = st.sidebar.checkbox("Mostra legenda")

folder_pratica = st.sidebar.selectbox(
    "Seleziona pratica",
    list(Path("pratiche").glob("*"))
)

p = Pratica(folder_pratica)
calls = p.calls

ok_to_show = ["e181ef3f-8b69-4114-96f9-adc71ce5ede3","99861b54-81f7-4b7b-8b5c-8300f28f2fb5","e573dba8-6276-4999-8533-965d901d34c7","9e0e793e-9610-4cef-bcb9-72d57df98900","17e2d03e-25e6-42e3-bcbe-d5b298d8c12f","63694915-4e5c-44cd-b632-3355d22f0270","3670cd79-8136-43cc-b47b-dbe72683c237","9fac6629-f287-40a0-8fef-6f10582d2cdb","d7966d93-30fa-4a86-a9e1-7faeddcdd45b","c0aff848-e134-4da3-853f-0756cd35fab3","a5d10646-d9fb-4256-9656-5580a21c6793","3cd3d86f-b37e-4a34-9af6-b1b373e2cda5","7294748d-46d3-4144-bb18-730514f9f3fa","5ce7d519-5f98-4e40-97a2-41fc78ea955a","e779f163-6de8-48bd-b449-c5cff0cef264","6cb60b07-b884-412e-a49e-d28b836ea7fe","f3cb0f23-c9cd-4015-95f7-36264953cb4a","7d68ec1e-d078-401d-8dd7-289a5c8c0cce","8f7d8ee1-aedb-419a-94ed-58d1d5b8667f"]
call = st.sidebar.selectbox(
    "Seleziona chiamata",
    list(c.call_id for c in calls if c.call_id in ok_to_show)
)

call_obj = [c for c in calls if c.call_id == call]

speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, call_id = get_labels_value(row=0, data_list=call_obj)
print(speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, call_id)

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

st.header(f"{p.id_} / {call_obj[0].call_id}")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = px.pie(values=speaker1_values, names=speaker1_labels, color=speaker1_labels, color_discrete_map=colors,
                     title="Mood Operatore")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig)

    with col2:
        fig = px.pie(values=speaker2_values, names=speaker2_labels, color=speaker2_labels, color_discrete_map=colors,
                     title="Mood Debitore")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig)


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.header("Testo Operatore")

        for s in txt1.split("\n"):
            st.markdown(s, unsafe_allow_html=False)

    with col2:
        st.header("Mood Operatore")
        # print(call_obj[0].call_id, p.id_)
        # for c in get_category_indexes(categorization1):
        #     c.find_missing_tuples()
        # print(get_missing_tuples(get_category_indexes(categorization1), call_obj[0].speaker1_txt_len))
        for start, end, name, _ in get_category_indexes(categorization1):
            annotated_text((txt1[start:end + 1], name, colors[name]))
            st.text("")


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.header("Testo Debitore")
        for s in txt2.split("\n"):
            st.markdown(s, unsafe_allow_html=False)

    with col2:
        st.header("Mood Debitore")
        category_idx = get_category_indexes(categorization2)
        # missing_tuples = get_missing_tuples(get_category_indexes(categorization2), call_obj[0].speaker2_txt_len)
        # complete_tuples = sorted(category_idx + missing_tuples)
        # print("print", complete_tuples)
        # for tup in complete_tuples:
        #     try:
        #         print(call_obj[0].speaker2_txt[tup[0]:tup[1]], tup[2])
        #     except IndexError:
        #         print(call_obj[0].speaker2_txt[tup[0]:tup[1]])
        for start, end, name, _ in get_category_indexes(categorization2):
            annotated_text((txt2[start:end + 1], name, colors[name]))
            st.text("")
