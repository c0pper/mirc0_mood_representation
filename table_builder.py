"""
Per considerazioni di Vincenzo
"""

from pathlib import Path
from classes import Pratica

moods = ["sintonia","distacco","incertezza","preoccupazione","sconforto","rabbia"]
if __name__ == "__main__":
    pratiche = Path("pratiche")
    for p in pratiche.glob("*"):
        pratica = Pratica(p)
        for call in pratica.calls:
            print(f"{pratica.id_}_{call.call_id}")

            # print("\toperatore")
            speaker1_labels = []
            for cat in call.speaker1_categories:
                speaker1_labels.append(cat["name"])
            for m in moods:
                if m not in speaker1_labels:
                    call.speaker1_categories.append({"name": m, "score": 0.0})
            sorted_speaker1_categories = sorted(call.speaker1_categories, key=lambda x: x['name'])
            # print(sorted_speaker1_categories)
            # for cat in sorted_speaker1_categories:
            #     print(f'\t\t{cat["name"]}\t{cat["score"]}')

            # print("\tdebitore")
            speaker2_labels = []
            for cat in call.speaker2_categories:
                # print(cat)
                speaker2_labels.append(cat["name"])
            for m in moods:
                if m not in speaker2_labels:
                    call.speaker2_categories.append({"name": m, "score": 0.0})
            sorted_speaker2_categories = sorted(call.speaker2_categories, key=lambda x: x['name'])
            # print(sorted_speaker2_categories)
            # for cat in sorted_speaker2_categories:
                # print(f'\t\t{cat["name"]}\t{cat["score"]}')



            # print("oper")
            lines = {}
            for c1 in sorted_speaker1_categories:
                c1_name = c1["name"]
                c1_score = c1["score"]
                # print(c1_name, c1_score)

            # print("deb")
            for c2 in sorted_speaker2_categories:
                c2_name = c2["name"]
                c2_score = c2["score"]
                # print(c2_name, c2_score)
            # print("\toperatore\t\tdebitore")
            # print(f'{c1_name}\t{c1_score}\t{c2_name}\t{c2_score}')
            zippato = list(zip(sorted_speaker1_categories, sorted_speaker2_categories))
            # print(zippato)
            print("\toperatore\tdebitore")
            for coppia in zippato:
                operatore = coppia[0]
                debitore = coppia[1]
                print(f'{operatore["name"]}\t{operatore["score"]}\t{debitore["score"]}')
            print("")

