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
# SPECIAL_FORMS_SET = set(['define', 'if', 'cond', 'and', 'or', 'let', 'begin', 'lambda', 'quote', 'quasiquote', 'unquote', 'mu', 'define-macro', 'expect', 'unquote-splicing', 'delay', 'cons-stream', 'set!'])

def define_form(args, env):
    symbol = args.first
    # binding define
    if scheme_symbolp(symbol):
        validate_form(args, 2)
        unevaluated = args.rest.first # can be a value or a pair
        value = scheme_eval(unevaluated, env)
        env.define(symbol, value)
        return symbol
    # function define
    if scheme_listp(symbol) and scheme_symbolp(symbol.first):
        # (define (<name> [param] ...) <body> ...)
        func_name = symbol.first
        lambda_formal, lambda_body = symbol.rest, args.rest
        lambda_args = Pair(lambda_formal, lambda_body)
        func_pointer = lambda_form(lambda_args, env)
        env.define(func_name, func_pointer)
        return func_name
    
    raise SchemeError(f"{symbol} is not a definable symbol")

def quote_form(args, _= None):
    # the args of quote is an expression
    validate_form(args, 1, 1)
    return args.first

def begin_form(args, env):
    # tail context
    if args.rest is nil:
        return scheme_eval(args.first, env, True)
    scheme_eval(args.first, env)
    # if args.rest is nil:
    #     return value
    return begin_form(args.rest, env)

def lambda_form(args, env):
    # (lambda ([param]) <body>)
    validate_form(args, 2) # empty param pair still counts one len
    param = args.first
    body = args.rest
    validate_formals(param)
    return LambdaProcedure(param, body, env)


# #f is the only value that is false. 
# All other values are treated as true in a boolean context.

def and_form(args, env):
    # (and [test] ...)
    # Evaluate the tests in order, returning the first false value.
    # If no test is false, return the last test. 
    # If no arguments are provided, return #t.
    if args is nil:
        return True
    # tail context
    # also the last one
    if args.rest is nil:
        return scheme_eval(args.first, env, True)

    cur_bool = scheme_eval(args.first, env)
    if is_scheme_false(cur_bool):
        return cur_bool
    return and_form(args.rest, env)


def or_form(args, env):
    # Evaluate the tests in order, returning the first true value.
    # If no test is true and there are no more tests left, return #f.
    if args is nil:
        return False
    # tail context
    if args.rest is nil:
        return scheme_eval(args.first, env, True)

    cur_bool = scheme_eval(args.first, env)
    if is_scheme_true(cur_bool):
        return cur_bool
    return or_form(args.rest, env)


def if_form(args, env):
    # (if <predicate> <consequent> [alternative])
    validate_form(args, 2, 3)
    predicate_expr, cons_expr, alter_expr = args.first, args.rest.first, args.rest.rest.first
    predicate_value = scheme_eval(predicate_expr, env)
    # tail context
    if is_scheme_true(predicate_value):
        return scheme_eval(cons_expr, env, True)
    else:
        return scheme_eval(alter_expr, env, True)


def cond_form(args, env):
    # (cond <clause> ...)
        # (<test> [expression] ...)
        # (else [expression] ...)
    def eval_exprs(test, exprs, env):
        if exprs is nil:
            return test
        return begin_form(exprs, env)
    
    clause = args.first
    validate_form(clause, 1)
    # test case
    if clause.first == 'else':
        if not args.rest is nil:
            raise SchemeError("incorrect else clause")
        return eval_exprs(True, clause.rest, env)
    else:
        test = scheme_eval(clause.first, env)
        if is_scheme_true(test):
            return eval_exprs(test, clause.rest, env)
        else:
            return cond_form(args.rest, env) if args.rest is not nil else None
        
        
def let_form(args, env):
    # (let ([binding] ...) <body> ...)
        # (<name> <expression>)
    def binding_form(bindings):
        if bindings is nil:
            return
        cur_binding = bindings.first
        validate_form(cur_binding, 2, 2)
        uneval_evalated_value = Pair('quote', Pair(scheme_eval(cur_binding.rest.first, env), nil))
        define_expr = Pair(cur_binding.first, Pair(uneval_evalated_value, nil))
        define_form(define_expr, new_env)
        binding_form(bindings.rest)
    
    new_env = Frame(env)
    binding_form(args.first)
    return begin_form(args.rest, new_env)

def mu_form(args, _: None):
    # (mu ([param] ...) <body> ...)
    validate_form(args, 2)
    formals = args.first
    body = args.rest
    validate_formals(formals)
    mu_procedure = MuProcedure(formals, body)
    return mu_procedure


def enumerate_form(args, env):
    # (enumerate (<list>)
    def helper(cur_list, count):
        if cur_list is nil:
            return
        cur_list.first = Pair(count, Pair(cur_list.first, nil))
        helper(cur_list.rest, count + 1)
        
    validate_form(args, 1, 1)
    list_expr = args.first.rest
    if list_expr is nil:
        return nil
    helper(list_expr.first, 0)
    return list_expr.first


def merge_form(args, env):
    # (merge <comparator> <list1> <list2>)
    def helper(comparator, longer, shorter):
        if longer is nil:
            return nil
        if shorter is nil:
            return longer
        comp_expr = Pair(comparator, Pair(longer.first, Pair(shorter.first, nil)))
        comp_res = scheme_eval(comp_expr, env)
        cur_pair = Pair(longer.first, Pair(shorter.first, nil))
        if is_scheme_false(comp_res):
            cur_pair.first, cur_pair.rest.first = cur_pair.rest.first, cur_pair.first
        cur_pair.rest.rest = helper(comparator, longer.rest, shorter.rest)
        return cur_pair


    validate_form(args, 3, 3)
    comparator = args.first
    list1 = args.rest.first.rest.first
    list2 = args.rest.rest.first.rest.first
    if len(list1) < len(list2):
        list1, list2 = list2, list1
    return helper(comparator, list1, list2)


# END PROBLEM 1/2/3

SPECIAL_FORMS_DICT = {
    'define': define_form,
    'quote': quote_form,
    'begin': begin_form,
    'lambda': lambda_form,
    'and': and_form,
    'or': or_form,
    'if': if_form,
    'cond': cond_form,
    'let': let_form,
    'mu': mu_form,
    'enumerate': enumerate_form,
    'merge': merge_form
}

