import numpy

from classes import Pratica
import matplotlib.pyplot as plt
from utils import get_labels_value


colors = {
    "distacco": "#00337C",
    "sintonia": "#1F8A70",
    "rabbia": "#E90064",
    "incertezza": "#607d8b",
    "preoccupazione": "#ff9800",
    "sconforto": "#7b1fa2"
}

quasar_colors = {
    "distacco": "indigo-8",
    "sintonia": "teal-6",
    "rabbia": "pink-13",
    "incertezza": "blue-grey-6",
    "preoccupazione": "orange-6",
    "sconforto": "purple-8"
}

def visualize(pratica: Pratica):

    data_list = []
    for c in pratica.calls:
        data_list.append(c)

    fig = plt.figure(layout='constrained', figsize=(8, int(len(data_list) * 4)))
    subfigs = fig.subfigures(len(data_list), 1, wspace=0.07)

    if isinstance(subfigs, numpy.ndarray):
        for row, subfig in enumerate(subfigs):
            speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, call_id = get_labels_value(row,
                                                                                                           data_list=data_list)

            axs = subfig.subplots(1, 2)
            subfig.suptitle(f"callID: {pratica.id_}_{call_id}")
            subfig.set_facecolor('0.85')

            axs[0].pie(speaker1_values, labels=speaker1_labels, autopct='%1.1f%%',
                       colors=[colors[v] for v in speaker1_labels])
            axs[0].set_title("Operatore")
            axs[1].pie(speaker2_values, labels=speaker2_labels, autopct='%1.1f%%',
                       colors=[colors[v] for v in speaker2_labels])
            axs[1].set_title("Debitore")

        # plt.savefig(f"{pratica.id_}.jpg")
        return plt

    else:
        row = 0
        speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, call_id = get_labels_value(row,
                                                                                                       data_list=data_list)
        figure, axis = plt.subplots(1, 2)
        figure.suptitle(f'callID: {pratica.id_}_{call_id}')

        axis[0].pie(speaker1_values, labels=speaker1_labels, autopct='%1.1f%%',
                    colors=[colors[v] for v in speaker1_labels])
        axis[0].set_title("Speaker1")

        axis[1].pie(speaker2_values, labels=speaker2_labels, autopct='%1.1f%%',
                    colors=[colors[v] for v in speaker2_labels])
        axis[1].set_title("Speaker2")
        # plt.savefig(f"{pratica.id_}.jpg")

        return plt
