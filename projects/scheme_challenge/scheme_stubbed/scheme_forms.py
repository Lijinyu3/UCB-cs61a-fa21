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
SPECIAL_FORMS = set(['define', 'if', 'cond', 'and', 'or', 'let', 'begin', 'lambda', 'quote', 'quasiquote', 'unquote', 'mu', 'define-macro', 'expect', 'unquote-splicing', 'delay', 'cons-stream', 'set!'])
# END PROBLEM 1/2/3
