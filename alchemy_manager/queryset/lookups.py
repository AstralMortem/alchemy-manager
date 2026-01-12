import operator


def _in(col, value):
    return col.in_(value)


def _contains(col, value):
    return col.contains(value)


def _startswith(col, value):
    return col.startswith(value)


def _endswith(col, value):
    return col.endswith(value)


LOOKUPS: dict[str, callable] = {
    "eq": operator.eq,
    "gt": operator.gt,
    "ge": operator.ge,
    "gte": operator.ge,  # alias
    "lt": operator.lt,
    "le": operator.le,
    "lte": operator.le,  # alias
    "ne": operator.ne,
    "in": _in,
    "contains": _contains,
    "startswith": _startswith,
    "endswith": _endswith,
}
