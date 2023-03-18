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
    elif scheme_listp(expr):
        # special forms
        if scheme_symbolp(expr.first) and expr.first in scheme_forms.SPECIAL_FORMS_DICT:
            return scheme_forms.SPECIAL_FORMS_DICT[expr.first](expr.rest, env)
        
        # call expression
        procedure = scheme_eval(expr.first, env)
        validate_procedure(procedure)
        args = expr.rest.map(lambda unevaled: scheme_eval(unevaled, env))
        return scheme_apply(procedure, args, env)
    
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
        return [pair_args.first] + get_args(pair_args.rest)
    
    def get_appliable_func(procedure, valued_args, env):
        if isinstance(procedure, BuiltinProcedure):
            if procedure.need_env:
                valued_args.append(env)
            return lambda :procedure.py_func(*valued_args)
        if isinstance(procedure, LambdaProcedure):
            # the parent of the new frame when the function is called
            # is the parent of this function
            # that is the frame where this function was defined
            lambda_env = Frame(procedure.env)
            iter_args = iter(valued_args)
            validate_form(args, len(procedure.formals), len(procedure.formals))
            procedure.formals.map(lambda p: lambda_env.define(p, next(iter_args)))
            return lambda :scheme_forms.begin_form(procedure.body, lambda_env)
        
        raise SchemeError("Unknown procedure")

    
    valued_args = get_args(args)
    func = get_appliable_func(procedure, valued_args, env)
    try:
        return func()
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
