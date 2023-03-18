import sys
import os

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms
import functools

##############
# Eval/Apply #
##############


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # BEGIN Problem 1/2
    
    # atomics expressions
    if scheme_atomp(expr):
        if self_evaluating(expr):
            return expr
        if scheme_symbolp(expr):
            return env.lookup(expr)

    # combinations (non-atmics expressions)
    elif scheme_listp(expr) and scheme_symbolp(expr.first):
        # special forms
        if expr.first in scheme_forms.SPECIAL_FORMS_DICT:
            return scheme_forms.SPECIAL_FORMS_DICT[expr.first](expr.rest, env)
        
        procedure = scheme_eval(expr.first, env)
        # call expression
        validate_procedure(procedure)
        args = expr.rest
        sub_env = Frame(env)
        return scheme_apply(procedure, args, sub_env)
    
    # invalid expressions
    else:
        raise SchemeError(f"Invalid input expression: {str(expr)}")
    # END Problem 1/2


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    # BEGIN Problem 1/2
    def get_args(pair_args):
        if pair_args is nil:
            return []
        return [scheme_eval(pair_args.first, env)] + get_args(pair_args.rest)
        # valued_args = []
        # while pair_args is not nil:
        #     valued_args.append(scheme_eval(pair_args.first, env))
        #     pair_args = pair_args.rest
        # return valued_args
    
    valued_args = get_args(args)
    if procedure.need_env:
        valued_args.append(env)
    try:
        return procedure.py_func(*valued_args)
    except TypeError:
        raise SchemeError("Incorrect arguments number")
    # END Problem 1/2


##################
# Tail Recursion #
##################

# Make classes/functions for creating tail recursive programs here!
# BEGIN Problem EC
"*** YOUR CODE HERE ***"
# END Problem EC


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not Unevaluated.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the extra credit."""
    validate_procedure(procedure)
    # BEGIN
    return val
    # END
