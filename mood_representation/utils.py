class Categorization:
    def __init__(self, name: str, label: str, score: int, frequency: float):
        self.name = name
        self.label = label
        self.score = score
        self.frequency = frequency
        self.scopes = []

    # def find_missing_tuples(self, stop, start=0):
    #     if self.scopes:
    #         # for s in self.scopes:
    #         #     s.scope_dict["name"] = self.name
    #         #     print(s.scope_dict)
    #         newList = []
    #         for s in self.scopes:
    #             if s.tuple[0] > start:
    #                 newList.append((start, s.tuple[0]))
    #             start = s.tuple[1] + 1
    #         # add any left over values
    #         if start < stop:
    #             newList.append((start, stop))
    #         return newList

class Scope:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.tuple = self.start, self.end
        self.scope_dict = {
            "start": self.start,
            "end": self.end,
        }
        self.operands = []

class Operand:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end


def get_labels_value(row: int, data_list: list = None, single_call=None):
    """
    Extracts the category labels and values for two speakers from a call's data.

    :param single_call: optional single call
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
    if not single_call:
        single_call = data_list[row]
    data = single_call.call_categories
    # extract the data for the speaker1 categories
    speaker1_data = data['speaker1_categories']
    speaker1_labels = [d['name'] for d in speaker1_data]
    speaker1_values = [d['score'] for d in speaker1_data]

    # extract the data for the speaker2 categories
    speaker2_data = data['speaker2_categories']
    speaker2_labels = [d['name'] for d in speaker2_data]
    speaker2_values = [d['score'] for d in speaker2_data]

    return speaker1_labels, speaker1_values, speaker2_labels, speaker2_values, single_call.call_id


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
        aggregate_rules_scores = []
        aggregate_scopes_scores = []
        for rule in category["rules"]:
            rule_score = rule["score"]
            aggregate_rules_scores.append(rule_score)

            for scope in rule["scope"]:
                scope_begin, scope_end = scope["begin"], scope["end"]
                scope_score = scope["score"]
                aggregate_scopes_scores.append(scope_score)

                operand_tuples =[]
                for op in scope["operands"]:
                    op_begin, op_end = op["begin"], op["end"]
                    operand_tuples.append(f"({op_begin}, {op_end})")

                category_indexes.add((scope_begin, scope_end, category_name, "_"))#sum(aggregate_scopes_scores))) #";".join(operand_tuples)))

    category_indexes = sorted(category_indexes, key=lambda x: x[0])
    return category_indexes