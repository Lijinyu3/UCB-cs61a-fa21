from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""

# BEGIN PROBLEM 1/2/3
SPECIAL_FORMS_SET = set(['define', 'if', 'cond', 'and', 'or', 'let', 'begin', 'lambda', 'quote', 'quasiquote', 'unquote', 'mu', 'define-macro', 'expect', 'unquote-splicing', 'delay', 'cons-stream', 'set!'])

def define_form(args, env):
    symbol = args.first
    # binding define
    if scheme_symbolp(symbol):
        validate_form(args, 2)
        unevaluated = args.rest.first # can be a value or a pair
        value = scheme_eval(unevaluated, env)
        env.define(symbol, value)
        return symbol
    if scheme_listp(symbol):
        raise SchemeError("Not done yet")
    
    raise SchemeError(f"{symbol} is not a definable symbol")

def quote_form(args, _= None):
    # the args of quote is an expression
    validate_form(args, 1, 1)
    return args.first
# END PROBLEM 1/2/3

SPECIAL_FORMS_DICT = {
    'define': define_form,
    'quote': quote_form
}

