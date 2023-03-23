class Pratica:
    def __init__(self, id_pratica):
        self.id_pratica = id_pratica
        self.calls = []

    def __repr__(self):
        return f"Pratica(id_pratica={self.id_pratica})"


class Call:
    def __init__(self, id_chiamata):
        self.id_chiamata = id_chiamata
        self.tags = []
    def __repr__(self):
        return f"Call(id_chiamata={self.id_chiamata})"


class Tag:
    def __init__(self, tag_name, speaker, text):
        self.tag_name = tag_name
        self.speaker = speaker
        self.text = text

    def __repr__(self):
        return f"Tag(tag_name={self.tag_name}, speaker={self.speaker}, text={self.text})"
