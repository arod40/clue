from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional, Tuple

from boolean_formula import parse_boolean_formula
from normalization import convert_to_cnf


@dataclass
class Variable:
    name: str
    value: Optional[bool] = None


@dataclass
class Literal:
    variable: Variable
    isneg: bool


@dataclass
class Clause:
    literals: List[Literal]


class CNF:
    def __init__(self, clauses: List[Clause]):
        self.clauses = clauses
        self.variables = {}
        for clause in clauses:
            for literal in clause.literals:
                self.variables[literal.variable.idx] = literal.variable

    def __str__(self):
        """
        Returns a string representation of this CNF object.
        """
        pass

    @staticmethod
    def parse(string: str) -> "CNF":
        """
        Parses a string representing an arbitrary Boolean formula into a CNF object.
        Input:
            string: str - a string representing an arbitrary Boolean formula
        Output:
            cnf: CNF - a CNF object representing the input string in conjunctive normal form
        """
        return convert_to_cnf(parse_boolean_formula(string))

    @staticmethod
    def is_clause_true(clause: Clause):
        return any(
            literal.variable.value is not None
            and (literal.variable.value or literal.isneg)
            for literal in clause.literals
        )

    def _remove_true_clauses(self):
        self.clauses = [
            clause for clause in self.clauses if not self.is_clause_true(clause)
        ]

    # DSL section for CNF manipulation
    def copy(self) -> "CNF":
        """
        Returns a copy of this CNF object.
        """
        return deepcopy(self)

    def add_clause(self, clause: List[Tuple[str, bool]]) -> "CNF":
        """
        Adds a clause to this CNF object.
        """
        assert all(
            [name in self.variables for name, _ in clause]
        ), f"Variable not found"

        clause = Clause(
            [Literal(self.variables[name], isneg) for name, isneg in clause]
        )
        if not self.is_clause_true(clause):
            self.clauses.append(clause)
        return self

    def set_variable_value(self, variable_name: str, value: bool) -> "CNF":
        """
        Sets the value of a variable in this CNF object.
        """

        # Checks
        assert variable_name in self.variables, f"Variable {variable_name} not found"
        assert (
            self.variables[variable_name].value is None
        ), f"Variable {variable_name} already has a value"

        # Set value
        self.variables[variable_name].value = value

        # Remove clauses that are now true
        self._remove_true_clauses()

        return self

    def set_variables_values(self, values: List[Tuple[str, bool]]) -> "CNF":
        """
        Sets the values of variables in this CNF object.
        """
        # Checks
        vars = set()
        for name, _ in values:
            assert name in self.variables, f"Variable {name} not found"
            assert name not in vars, f"Variable {name} assigned twice"
            assert (
                self.variables[name].value is None
            ), f"Variable {name} already has a value"

        # Set values
        for name, value in values:
            self.variables[name].value = value

        # Remove clauses that are now true
        self._remove_true_clauses()

        return self

    def satisfy(self) -> bool:
        """
        Tries to satisfy this CNF object. Returns True if it succeeds, False otherwise.
        """
        pass
