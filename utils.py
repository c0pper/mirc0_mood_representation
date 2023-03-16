class Categorization:
    def __init__(self, name: str, label: str, score: int, frequency: float):
        self.name = name
        self.label = label
        self.score = score
        self.frequency = frequency
        self.scopes = []

    def find_missing_tuples(self):
        if self.scopes:
            for s in self.scopes:
                s.scope_dict["name"] = self.name
                print(s.scope_dict)

class Scope:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.scope_dict = {
            "start": self.start,
            "end": self.end,
        }
        self.operands = []

class Operand:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end



def get_missing_tuples(list_of_tuples, stop, start=0):
    newList = []
    for tup in list_of_tuples:
        if tup[0] > start:
            newList.append((start, tup[0]))
        start = tup[1] +1
    # add any left over values
    if start < stop:
        newList.append((start, stop))
    return newList


def get_category_indexes(categorization: list) -> list:
    """
    Return a sorted list of unique (begin, end, category) tuples from a categorization list.

    :param categorization: A list of dictionaries representing categories with rules and scopes.
    :type categorization: list

    :return: A sorted list of unique tuples, each representing the beginning and end index of a scope,
        and the name of the category it belongs to.
    :rtype: list
    """
    category_indexes = set()
    for category in categorization:
        category_name = category["name"]
        category_obj = Categorization(category["name"], category["label"], category["score"], category["frequency"])
        for rule in category["rules"]:
            for scope in rule["scope"]:
                scope_begin, scope_end = scope["begin"], scope["end"]
                scope_obj = Scope(scope_begin, scope_end)
                for op in scope["operands"]:
                    op_begin, op_end = op["begin"], op["end"]
                    operand_obj = Operand(op_begin, op_end)
                    scope_obj.operands.append(operand_obj)
                category_obj.scopes.append(scope_obj)
                category_obj.scopes.sort(key=lambda x: x.start)
                category_indexes.add((scope_begin, scope_end, category_name))
        # category_indexes.add(category_obj)
    category_indexes = sorted(category_indexes)
    return category_indexes