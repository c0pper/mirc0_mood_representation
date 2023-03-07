import json
import gzip
from pathlib import Path
from typing import Union


def get_call_id(file_path: Path) -> str:
    file_name = file_path.name
    file_name = str(file_name)
    call_id = file_name.split("_")[2]
    call_id = call_id.split("--")[0]
    return call_id


class Pratica:
    def __init__(self, folder_path: Union[Path, str]):
        self.folder_path = Path(folder_path) if isinstance(folder_path, str) else folder_path
        self.ctx_files = self.get_ctx_files()
        self.id_ = self.ctx_files[0].stem.split("_")[0]
        self.calls = self.get_calls()

    def get_ctx_files(self) -> list:
        file_list = self.folder_path.glob("*.ctx.json.gz")
        return list(file_list)

    def get_calls(self) -> list:
        calls = []
        for i in range(len(self.ctx_files)):
            for j in range(i + 1, len(self.ctx_files)):
                if get_call_id(self.ctx_files[i]) in get_call_id(self.ctx_files[j]) or get_call_id(self.ctx_files[j]) \
                        in get_call_id(self.ctx_files[i]):
                    call = Call(call_id=get_call_id(self.ctx_files[i]), speaker1_path=self.ctx_files[i],
                                speaker2_path=self.ctx_files[j])
                    calls.append(call)
        return calls


class Call:
    def __init__(self, call_id: str, speaker1_path: Path, speaker2_path: Path):
        self.call_id = call_id

        self.speaker1_path = speaker1_path
        self.speaker1_categorization = self.get_categorization(speaker1_path)
        self.speaker1_categories = [{"name": i.get("name"), "score": i.get("score")} for i in
                                    self.speaker1_categorization]
        self.norm_scores(self.speaker1_categories)

        self.speaker2_path = speaker2_path
        self.speaker2_categorization = self.get_categorization(speaker2_path)
        self.speaker2_categories = [{"name": i.get("name"), "score": i.get("score")} for i in
                                    self.speaker2_categorization]
        self.norm_scores(self.speaker2_categories)

        self.call_categories = {
            "speaker1_categories": self.speaker1_categories,
            "speaker2_categories": self.speaker2_categories
        }

    @staticmethod
    def norm_scores(categories: list):
        raw_scores = [i.get("score") for i in categories]
        for i in categories:
            score = i.get("score")
            if score:
                i["score"] = float(score) / sum(raw_scores)

    @staticmethod
    def get_categorization(file_path:Path) -> list:
        with gzip.open(file_path, "rb") as gzip_file:
            # Decode the compressed data into a string
            json_str = gzip_file.read().decode("utf-8")

            # Load the JSON data from the string
            json_data = json.loads(json_str)
            categorization = json_data["match_info"]["rules"]["categorization"]
            return categorization

    def __str__(self):
        return f"ID: {self.call_id}, Speaker1: {self.speaker1_path.name}, Speaker2: {self.speaker2_path.name}"

    def __repr__(self):
        return f"call_id: {self.call_id}, speaker1_path: {self.speaker1_path.name}, speaker2_path: {self.speaker2_path.name})"