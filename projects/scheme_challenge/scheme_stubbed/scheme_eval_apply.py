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
    def get_procedure_and_args(expr):
        # special forms
        if scheme_symbolp(expr.first) and expr.first in scheme_forms.SPECIAL_FORMS_DICT:
            proc = scheme_forms.SPECIAL_FORMS_DICT[expr.first]
            return proc, expr.rest
        # call expr
        proc = scheme_eval(expr.first, env)
        validate_procedure(proc)
        args = expr.rest.map(lambda unevaluated: scheme_eval(unevaluated, env))
        return proc, args

    
    # atomics expr
    if self_evaluating(expr):
        return expr
    if scheme_symbolp(expr):
        return env.lookup(expr)
    # combinations (non-atomic expr)
    if scheme_listp(expr):
        proc, args = get_procedure_and_args(expr)
        return scheme_apply(proc, args, env)
        
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
        if callable(procedure):
            return lambda :procedure(args, env)
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
        if isinstance(procedure, MuProcedure):
            # When the procedure this form creates is called,
            # the call frame will extend the environment the mu is called in.
            mu_env = Frame(env)
            iter_args = iter(valued_args)
            validate_form(args, len(procedure.formals), len(procedure.formals))
            procedure.formals.map(lambda p: mu_env.define(p, next(iter_args)))
            return lambda :scheme_forms.begin_form(procedure.body, mu_env)
        
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
class Unevaluated:
    def __init__(self, expr, env) -> None:
        self.expr = expr
        # self.arguments = arguments
        self.env = env

def is_tail_call(expr, env):
    if not scheme_listp(expr) or expr is nil:
        return False
    proc = expr.first
    if not scheme_symbolp(proc):
        return False
    if proc in scheme_forms.SPECIAL_FORMS_DICT:
        return False
    if isinstance(scheme_eval(proc, env), BuiltinProcedure):
        return False
    return True

def optimize_scheme_eval(unoptimized_eval):
    def optimized_eval(expr, env, tail_context= False):
        if tail_context and is_tail_call(expr, env):
            return Unevaluated(expr, env)
        if not isinstance(expr, Unevaluated):
            expr = unoptimized_eval(expr, env)
        while isinstance(expr, Unevaluated) and not tail_context:
            expr = unoptimized_eval(expr.expr, expr.env)
        return expr
    return optimized_eval
# END Problem EC


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not Unevaluated.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the extra credit."""
    validate_procedure(procedure)
    # BEGIN
    result =  scheme_apply(procedure, args, env)
    if isinstance(result, Unevaluated):
        return scheme_eval(result, result.env)
    return result
    # END

# tail call optimization
scheme_eval = optimize_scheme_eval(scheme_eval)