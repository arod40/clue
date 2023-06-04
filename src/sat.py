from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Variable:
    name: str
    idx: int

@dataclass
class Literal:
    variable: Variable
    isneg: bool

@dataclass
class Assignment:
    variable: Variable
    value: bool

@dataclass
class Clause:
    literals: List[Literal]

class CNF:
    def __init__(self, clauses: List[Clause]):
        self.clauses = clauses

    @staticmethod
    def parse(string: str):
        """
        Parses a string representing an arbitrary Boolean formula into a CNF object.
        Input:
            string: str - a string representing an arbitrary Boolean formula
        Output:
            cnf: CNF - a CNF object representing the input string in conjunctive normal form
        """
        pass

    def copy(self):
        """
        Returns a copy of this CNF object.
        """
        pass

    def __str__(self):
        """
        Returns a string representation of this CNF object.
        """
        pass


    def satisfiable(self) -> Tuple[bool, Optional[List[Assignment]]]:
        """
        Returns True if this CNF object is satisfiable, False otherwise.
        """
        pass

