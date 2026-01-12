# miniorm/q.py
from sqlalchemy import and_, or_, not_
from .lookups import LOOKUPS


class Q:
    def __init__(self, **kwargs):
        self.children = []
        self.connector = and_
        self.negated = False

        for key, value in kwargs.items():
            self.children.append((key, value))

    def __and__(self, other):
        q = Q()
        q.children = [self, other]
        q.connector = and_
        return q

    def __or__(self, other):
        q = Q()
        q.children = [self, other]
        q.connector = or_
        return q

    def __invert__(self):
        q = Q()
        q.children = [self]
        q.negated = True
        return q

    def resolve(self, model):
        expressions = []

        for child in self.children:
            if isinstance(child, Q):
                expressions.append(child.resolve(model))
            else:
                key, value = child
                field, lookup = key.split("__", 1) if "__" in key else (key, "eq")
                column = getattr(model, field)
                expressions.append(LOOKUPS[lookup](column, value))

        expr = self.connector(*expressions)
        return not_(expr) if self.negated else expr
