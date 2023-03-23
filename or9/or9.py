import pandas as pd
from classes import Pratica, Call, Tag


def get_pratiche_from_excel(df):
    # creazione oggetti Pratica per ogni id pratica
    ids_pratica = df["IDPRT"].unique()
    pratiche = [Pratica(id_pratica=i) for i in ids_pratica]

    # popolazione p.calls per ogni pratica
    for p in pratiche:

        id_chiamate = df[df["IDPRT"] == p.id_pratica]["idchiamata"].unique()
        p.calls = [Call(id_chiamata=i) for i in id_chiamate]

    # popolazione call.tags per ogni call in ogni pratica
    for p in pratiche[:5]:
        for call in p.calls:
            call_df = df[df["idchiamata"] == call.id_chiamata]
            call.tags = [Tag(tag_name=row.TAG, speaker=row.Speaker, text=row.Text) for row in call_df.itertuples()]

    return pratiche


if __name__ == '__main__':
    df = pd.read_excel("tags_da_taggatori_dic_gen.xlsx")
    pratiche = get_pratiche_from_excel(df)

    for p in pratiche[:5]:
        print(f"{p.id_pratica}")
        for call in p.calls:
            print(f"\t{call.id_chiamata}")
            print(f"\t\t{call.tags}")