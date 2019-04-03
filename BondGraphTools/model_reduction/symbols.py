import logging
import sympy

logger = logging.getLogger(__name__)


class Parameter(sympy.Symbol):
    """ Global parameter class.

    Global parameters are uniquely specified by name.
    """
    __slot__ = ['value']
    is_number = True
    is_nonzero = True
    is_finite = True
    is_constant = True

    def __new__(cls, name, value=None, **assumptions):
        obj = super().__new__(cls, name, **assumptions)
        obj.value = value
        return obj

    def evalf(self, *args):
        if self.value is None:
            return super().evalf()
        else:
            return sympy.Float(self.value).evalf(*args)

    # def __repr__(self):
    #     return self.name
    #
    # def __str__(self):
    #     return self.name

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        if self is other:
            return True

        if self.value is None:
            if other.__class__ is Parameter and other.value is not None:
                return False
            else:
                return super().__eq__(other)
        else:
            if other.__class__ is Parameter:
                return super().__eq__(other) and self.value == other.value

        return False


class Variable(sympy.Symbol):
    """Local Variable Class.

    Local variables are symbolic variables like $x_0$ that are associated with
    a particular chart.

    """
    order = 5
    default_prefix = 'x'

    def __hash__(self):
        return super().__hash__()


class DVariable(sympy.Symbol):
    order = 2
    default_prefix = 'dx'

    def __hash__(self):
        return super().__hash__()

    def __new__(cls, name, **assumptions):

        if isinstance(name, str):
            obj = super().__new__(cls, f"{name}", **assumptions)
        elif isinstance(name, Variable):
            obj = super().__new__(cls, f"d{str(name)}", **assumptions)
        return obj


class Effort(sympy.Symbol):
    order = 3
    default_prefix = 'e'

    def __hash__(self):
        return super().__hash__()


class Flow(sympy.Symbol):
    order = 4
    default_prefix = 'f'

    def __hash__(self):
        return super().__hash__()


class Control(sympy.Symbol):
    order = 6
    default_prefix = 'u'

    def __hash__(self):
        return super().__hash__()


class Output(sympy.Symbol):
    order = 1
    default_prefix = 'y'

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, other):
        return self is other


def canonical_order(symbol):
    """
    Canonical ordering of Energetic Variables.
    Symbols of the form "x_0", "dx_3" are assigned a triple such that for any n, or for i > j
        y_n > dx_n > e_i > f_i > e_j > x_n > u_n


    Args:
        symbol: The symbol from which t generate a key.

    Returns: 3-tuple of int's
    """
    try:
        prefix, index = symbol.name.split('_')
    except ValueError:
        return 4, 0, 0

    if prefix == 'y':
        return 0, int(index), 0
    elif prefix == 'dx':
        return 0, int(index), 1
    elif prefix == 'e':
        return 1, int(index), 0
    elif prefix == 'f':
        return 1, int(index), 1
    elif prefix == 'x':
        return 2, int(index), 0
    elif prefix == 'u':
        return 2, int(index), 1
    else:
        return 3, 0, 0


def evaluate(equation):
    """Tries to evaluate an equation"""
    try:
        if equation.is_Atom:
            return equation.evalf()
    except AttributeError:
        pass
    except TypeError:
        return equation

    new_args = [evaluate(a) for a in equation.args]

    return equation.__class__(*new_args)
