import numpy

from classes import Pratica
import matplotlib.pyplot as plt


def get_labels_value(data_list: list, row: int):
    """
    Extracts the category labels and values for two speakers from a call's data.

    :param data_list: A list of CallData objects, each containing call data.
    :param row: An integer representing the row number of the call data to extract.

    :return: A tuple containing the following five items:
             - A list of category labels for speaker1.
             - A list of category values for speaker1.
             - A list of category labels for speaker2.
             - A list of category values for speaker2.
             - A string representing the call ID.

    :raises IndexError: If the specified row number is out of bounds for the data list.

    Example usage:
        data = [CallData(call_id='123', call_categories={        ...              'speaker1_categories': [{'name': 'Category1', 'score': 0.5},        ...                                      {'name': 'Category2', 'score': 0.3}],
        ...              'speaker2_categories': [{'name': 'Category3', 'score': 0.2},        ...                                      {'name': 'Category4', 'score': 0.4}]})]
        get_labels_value(data, 0)
        (['Category1', 'Category2'], [0.5, 0.3], ['Category3', 'Category4'], [0.2, 0.4], '123')
    """
    call = data_list[row]
    data = call.call_categories
    # extract the data for the speaker1 categories
    speaker1_data = data['speaker1_categories']
    speaker1_labels = [d['name'] for d in speaker1_data]
    speaker1_values = [d['score'] for d in speaker1_data]

    # extract the data for the speaker2 categories
    speaker2_data = data['speaker2_categories']
    speaker2_labels = [d['name'] for d in speaker2_data]
    speaker2_values = [d['score'] for d in speaker2_data]

    return speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, call.call_id


colors = {
    "distacco": "#00337C",
    "sintonia": "#1F8A70",
    "rabbia": "#E90064",
    "incertezza": "#93C6E7",
    "preoccupazione": "#FF8B13",
    "sconforto": "#804674"
}

def visualize(pratica: Pratica):

    data_list = []
    for c in pratica.calls:
        data_list.append(c)

    fig = plt.figure(layout='constrained', figsize=(8, int(len(data_list) * 4)))
    subfigs = fig.subfigures(len(data_list), 1, wspace=0.07)

    if isinstance(subfigs, numpy.ndarray):
        for row, subfig in enumerate(subfigs):
            speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, call_id = get_labels_value(data_list,
                                                                                                           row)

            axs = subfig.subplots(1, 2)
            subfig.suptitle(f"callID: {pratica.id_}_{call_id}")
            subfig.set_facecolor('0.85')

            axs[0].pie(speaker1_values, labels=speaker1_labels, autopct='%1.1f%%',
                       colors=[colors[v] for v in speaker1_labels])
            axs[0].set_title("Speaker1")
            axs[1].pie(speaker2_values, labels=speaker2_labels, autopct='%1.1f%%',
                       colors=[colors[v] for v in speaker2_labels])
            axs[1].set_title("Speaker2")

        plt.savefig(f"{pratica.id_}.jpg")

    else:
        row = 0
        speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, call_id = get_labels_value(data_list, row)
        figure, axis = plt.subplots(1, 2)
        figure.suptitle(f'callID: {pratica.id_}_{call_id}')

        axis[0].pie(speaker1_values, labels=speaker1_labels, autopct='%1.1f%%',
                    colors=[colors[v] for v in speaker1_labels])
        axis[0].set_title("Speaker1")

        axis[1].pie(speaker2_values, labels=speaker2_labels, autopct='%1.1f%%',
                    colors=[colors[v] for v in speaker2_labels])
        axis[1].set_title("Speaker2")
        plt.savefig(f"{pratica.id_}.jpg")
