#!/usr/bin/env python
# encoding: utf-8
"""
@version: 2.7
@author: hyzhan
@file: test_ply.py
@time: 2017-2-23 16:12:00
"""

from ply import lex
from ply import yacc
from ply.lex import TOKEN

tokens = (
    "OPEN",
    "LAMP",
    "USELESS",
    "NOT"
)
# t_ignore = r"\t"
t_NOT=(
    r"(do\snot|don\'t)"
)
t_OPEN=(
    r"open | start"
)

t_LAMP=(
    r"lamp"
)
t_USELESS=(
    r"(?!"+t_NOT+r")"+r"(?!"+t_OPEN+r")"+r"(?!"+t_LAMP+r")"+r"[a-z]+"
)

@TOKEN(t_USELESS)
# def t_USELESS(t):
#     r"(?!" + t_OPEN + r")" + r"(?!" + t_LAMP + r")" + r"[a-z]*"
#     return t

# def t_error(t):
#     raise TypeError("Unknown text '%s'" % (t.value,))
def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer=lex.lex()


class Lamp(object):
    def __init__(self, action, object):
        self.action = action
        self.object = object

    def __repr__(self):
        return "Lamp(%r, %r)" % (self.action, self.object)

# def p_useless_word(p):
#     """
#     useless_word :
#     useless_word : useless_word useless
#     useless_word : action_list useless
#     """
#     if len(p) == 3:
#         p[0] = p[1]
#     else:
#         p[0]={}

def p_action_list(p):
    """
    action_list :
    action_list : action
    action_list : action_list action
    """
    if len(p)==2:
        p[0] = {p[1].action: p[1].object}
    elif len(p)==3:
        p[0]=dict({p[2].action: p[2].object},**p[1])
    else:
        p[0]={}

def p_deal_useless(p):
    """
    action : action useless
    """
    p[0] = p[1]

def p_deal_useless2(p):
    """
    action : useless action
    """
    p[0] = p[2]

def p_single_action(p):
    """
    action : open lamp
    action : NOT open lamp
    """
    if len(p)==3:
        p[0] = Lamp('open', p[2])
    if len(p)==4:
        p[0] = Lamp('hold', p[3])

def p_single_object(p):
    """
    lamp : LAMP
    lamp : LAMP useless
    """
    p[0] = p[1]

def p_single_open(p):
    """
    open : OPEN
    open : OPEN useless
    """
    p[0] = p[1]

def p_single_useless(p):
    """
    useless : USELESS
    """
    p[0] = p[1]

def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))

yacc.yacc()

######

def lamp_action(s):
    action_dicts = yacc.parse(s,lexer=lexer)
    # action_dicts = yacc.parse(s,lexer=lexer,debug=True)
    return action_dicts


test=[
    "open lamp",
"open lamp open lamp",
"open lamp asd asds fdsfvd",
    "fdsfvd sdf open lamp",
"fdsfvd sdf open lamp egc svd",
"open lamp asd open lamp",
"wade open lamp asd open lamp wad",
"please open the lamp",
    'please do not open the lamp'
]
if __name__ == "__main__":
    # lexer.input("open lamp sd open lamp sd sa")
    # for token in lexer:
    #     print token
    num=0
    for sentenses in test:
        print num,test[num]
        print "result:",lamp_action(sentenses)
        num+=1
    print "All tests passed."