from typing import Iterable, Dict


def repeated_item_names_gen(item_names: Iterable[str], item_counts: Dict[str, int]):
    """
    Generator that repeatedly yields the items names in `item_names` as many times as the count of that item name in
    `item_counts`.
    """
    for item_name in item_names:
        item_count = item_counts[item_name]
        for _ in range(item_count):
            yield item_name


def concat_unique_dicts(*dicts: Dict[str, int]):
    """
    Helper for safely concatenating dicts that should have both unique keys and unique values.
    Checks that the concatenated dict has the correct length and number of unique values.
    """
    expected_length = sum(map(len, dicts))
    concatenated = {}
    for d in dicts:
        concatenated.update(d)
    if expected_length != len(concatenated):
        raise RuntimeError(f"Unique dict concatenation contains duplicate keys, expected concatenated dict length was"
                           f" {expected_length}, but the actual length was {len(concatenated)}")
    if expected_length != len(set(concatenated.values())):
        raise RuntimeError(f"Unique dict concatenation contains duplicate values, expected number of unique values was"
                           f" {expected_length}, but the actual number of unique values was {len(concatenated)}")
    return concatenated
