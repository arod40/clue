from itertools import product
from typing import Tuple

from boolean_formula import *
import visitor


class PushDownNegationsVisitor:
    @visitor.on("formula")
    def visit(self, formula: BooleanFormula, carry: bool) -> BooleanFormula:
        """
        Returns a formula where all negations are pushed down to the variables.
        This is the first step in the conversion to CNF."""
        pass

    @visitor.when(Conjunction)
    def visit(self, formula: Conjunction, carry: bool) -> BooleanFormula:
        return Disjunction(
            self.visit(formula.left, carry), self.visit(formula.right, carry)
        )

    @visitor.when(Disjunction)
    def visit(self, formula: Disjunction, carry: bool) -> BooleanFormula:
        return Conjunction(
            self.visit(formula.left, carry), self.visit(formula.right, carry)
        )

    @visitor.when(Negation)
    def visit(self, formula: Negation, carry: bool) -> BooleanFormula:
        return self.visit(formula.formula, not carry)

    @visitor.when(Variable)
    def visit(self, formula: Variable, carry: bool) -> BooleanFormula:
        if carry:
            return Negation(formula)
        else:
            return formula


class PullUpConjunctionsVisitor:
    @visitor.on("formula")
    def visit(self, formula: BooleanFormula) -> Tuple[BooleanFormula, bool]:
        """
        Returns a tuple (formula, is_conjunct) where is_conjunct is True if the formula
        is a conjunction of two formulas, and False otherwise; and formula is
        in CNF.
        Assumes that negations have been pushed down, i.e., only applied to plain
        variables.
        This is the second step in the conversion to CNF."""
        pass

    @visitor.when(Conjunction)
    def visit(self, formula: Conjunction) -> Tuple[BooleanFormula, bool]:
        return Conjunction(self.visit(formula.left), self.visit(formula.right)), True

    @visitor.when(Disjunction)
    def visit(self, formula: Disjunction) -> Tuple[BooleanFormula, bool]:
        cnf_left, is_left_conjunct = self.visit(formula.left)
        cnf_right, is_right_conjunct = self.visit(formula.right)

        if is_left_conjunct or is_right_conjunct:
            left = [cnf_left.left, cnf_left.right] if is_left_conjunct else [cnf_left]
            right = (
                [cnf_right.left, cnf_right.right] if is_right_conjunct else [cnf_right]
            )
            clauses = list(product(left, right))

            cnf_formula = Conjunction(*clauses[:2])
            for clause in clauses[2:]:
                cnf_formula = Conjunction(cnf_formula, clause)

            return cnf_formula, True

        else:
            return Disjunction(cnf_left, cnf_right), False

    @visitor.when(Negation)
    def visit(self, formula: Negation) -> Tuple[BooleanFormula, bool]:
        return formula, False

    @visitor.when(Variable)
    def visit(self, formula: Variable) -> Tuple[BooleanFormula, bool]:
        return formula, False


def convert_to_cnf(formula: BooleanFormula) -> BooleanFormula:
    """
    Returns a formula in CNF.
    """
    return PullUpConjunctionsVisitor().visit(PushDownNegationsVisitor().visit(formula))[
        0
    ]
