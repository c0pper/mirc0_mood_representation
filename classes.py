import json
import gzip
from pathlib import Path
from typing import Union
import re


def get_call_id(file_path: Path) -> str:
    file_name = file_path.name
    file_name = str(file_name)
    call_id = file_name.split("_")[2]
    call_id = call_id.split("--")[0]
    return call_id


def find_annotation_json(ctx_files, text_path: Path) -> Path:
    for j in ctx_files:
        if str(j.stem).split(".")[0] == text_path.stem:
            return j


def find_original_txt(txt_files, json_path: Path) -> Path:
    for t in txt_files:
        if t.stem == str(json_path.stem).split(".")[0]:
            return t

class Domain:
    def __init__(self, name):
        self.name = name
        self.frequency = 0
        self.rules = list()
        self.score = 0

    def get_domain_score(self):
        return sum([rule.score  for rule in self.rules])


class Rule:
    def __init__(self):
        self.label = ""
        self.scopes = list()
        self.score = 0

    def get_rule_score(self):
        return sum([scope.score  for scope in self.scopes])


class Scope:
    def __init__(self):
        self.score = 0
        self.begin = 0
        self.end = 0
        self.operands = list()

    def get_scope_text(self, call_txt):
        return call_txt[self.begin:self.end+1]


class Operand:
    def __init__(self):
        self.begin = 0
        self.end = 0

    def get_operand_text(self, call_txt):
        return call_txt[self.begin:self.end+1]


class Pratica:
    def __init__(self, folder_path: Union[Path, str]):
        self.folder_path = Path(folder_path) if isinstance(folder_path, str) else folder_path
        self.ctx_files = self.get_ctx_files()
        self.txt_files = self.get_txt_files()
        self.id_ = self.ctx_files[0].stem.split("_")[0]
        self.calls = self.get_calls()

    def get_ctx_files(self) -> list:
        file_list = self.folder_path.glob("json/*.ctx.json.gz")
        return list(file_list)

    def get_txt_files(self) -> list:
        file_list = self.folder_path.glob("txt/*.txt")
        return list(file_list)

    def get_calls(self) -> list:
        calls = []
        for i in range(len(self.ctx_files)):
            for j in range(i + 1, len(self.ctx_files)):
                if get_call_id(self.ctx_files[i]) in get_call_id(self.ctx_files[j]) or get_call_id(self.ctx_files[j]) \
                        in get_call_id(self.ctx_files[i]):
                    call = Call(self, call_id=get_call_id(self.ctx_files[i]), speaker1_json_path=self.ctx_files[i],
                                speaker2_json_path=self.ctx_files[j])
                    calls.append(call)
        return calls


class Call:
    def __init__(self, pratica: Pratica, call_id: str, speaker1_json_path: Path, speaker2_json_path: Path):
        self.pratica = pratica
        self.call_id = call_id

        # Speaker 1
        self.speaker1_json_path = speaker1_json_path
        self.speaker1_txt_path = find_original_txt(pratica.txt_files, speaker1_json_path)
        with open(self.speaker1_txt_path, "r", encoding="utf8") as txt:
            self.speaker1_txt = txt.read()
            self.speaker1_txt_len = len(self.speaker1_txt)
        self.speaker1_categorization = self.get_categorization(speaker1_json_path)
        self.speaker1_categories = [{"name": i.get("name"), "score": i.get("score")} for i in
                                    self.speaker1_categorization]
        self.speaker1_domain_objects = self.collect_domain_objects(self.speaker1_categorization)
        self.norm_scores(self.speaker1_categories)

        # Speaker 2
        self.speaker2_json_path = speaker2_json_path
        self.speaker2_txt_path = find_original_txt(pratica.txt_files, speaker2_json_path)
        with open(self.speaker2_txt_path, "r", encoding="utf8") as txt:
            self.speaker2_txt = txt.read()
            self.speaker2_txt_len = len(self.speaker2_txt)
        self.speaker2_categorization = self.get_categorization(speaker2_json_path)
        self.speaker2_categories = [{"name": i.get("name"), "score": i.get("score")} for i in
                                    self.speaker2_categorization]
        self.speaker2_domain_objects = self.collect_domain_objects(self.speaker2_categorization)
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

    @staticmethod
    def collect_domain_objects(call_categorization):
        domain_objects = []
        for cat in call_categorization:
            domain = Domain(cat["name"])
            domain.frequency = cat["frequency"]
            domain.score = cat["score"]
            # print(domain.name)

            for rule in cat["rules"]:
                rule_obj = Rule()
                rule_obj.label = rule["label"]
                domain.rules.append(rule_obj)
                # print(f'\trule label "{rule_obj.label}", rule score {rule_obj.score}')

                for scope in rule["scope"]:
                    scope_begin = scope["begin"]
                    scope_end = scope["end"]
                    scope_score = scope["score"]

                    scope_obj = Scope()
                    scope_obj.begin = scope_begin
                    scope_obj.end = scope_end
                    scope_obj.score = scope_score
                    rule_obj.scopes.append(scope_obj)

                    # print(f"\t\tscope range {scope_obj.begin} - {scope_obj.end}, score {scope_obj.score}")
                    # print(f"\t\tscope text: {scope_obj.get_scope_text(call.speaker2_txt)}")
                    # print("\t\t\tOperands")
                    for op in scope["operands"]:
                        op_begin = op["begin"]
                        op_end = op["end"]

                        op_obj = Operand()
                        op_obj.end = op_end
                        op_obj.begin = op_begin
                        scope_obj.operands.append(op_obj)
                        # print(f"\t\t\t\toperand range {op_obj.begin} - {op_obj.end}")
                        # print(f"\t\t\t\toperand text: {op_obj.get_operand_text(call.speaker2_txt)}")
                rule_obj.score = rule_obj.get_rule_score()
                # print(f"\trule score{rule_obj.score}")
            domain_objects.append(domain)
            # print(f"domain score {domain.score}")
        return domain_objects

    def __str__(self):
        return f"ID: {self.call_id}, Speaker1_json: {self.speaker1_json_path.name}, " \
               f"Speaker2_json: {self.speaker2_json_path.name}, Speaker1_txt: {self.speaker1_txt_path.name}, " \
               f"Speaker2_txt: {self.speaker2_txt_path.name}"

    def __repr__(self):
        return f"call_id: {self.call_id}, speaker1_json_path: {self.speaker1_json_path.name}, " \
               f"speaker2_json_path: {self.speaker2_json_path.name}, speaker1_txt_path: {self.speaker1_txt_path.name}" \
               f", speaker2_txt_path: {self.speaker2_txt_path.name})"
