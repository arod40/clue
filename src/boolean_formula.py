class BooleanFormula:
    pass


class BinaryBooleanFormula(BooleanFormula):
    def __init__(self, left: BooleanFormula, right: BooleanFormula):
        self.left = left
        self.right = right


class Conjunction(BinaryBooleanFormula):
    pass


class Disjunction(BinaryBooleanFormula):
    pass


class Negation(BooleanFormula):
    def __init__(self, formula: BooleanFormula):
        self.formula = formula


class Variable(BooleanFormula):
    def __init__(self, name: str):
        self.name = name


def parse_boolean_formula(string: str) -> BooleanFormula:
    """Parses a boolean formula from a string."""
    pass
