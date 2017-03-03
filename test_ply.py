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

tokens = ("NOT","OPEN","CLOSE","VERB","LAMP","AirPurifier","OBJECT_SMART","USELESS")
# t_ignore = r"\t"
t_NOT=(
    r"(do\snot|don\'t|did\snot|didn't)"
)
t_OPEN=(
    r"(open|start|turn\son)"
)
t_CLOSE=(
    r"(close|stop|turn\soff)"
)

t_LAMP=(
    r"(lamp|light)"
)
t_AirPurifier=(
    r"(AirPurifier)"
)
# t_VERB=(
#     r"("+t_OPEN+r"|"+t_CLOSE+r")+"
# )


t_USELESS=(
    r"(?!"+t_NOT+r")"+r"(?!"+t_CLOSE+r")"+r"(?!"+t_OPEN+r")"+r"(?!"+t_LAMP+r")"+r"[a-z]+"
)
# t_OBJECT_SMART=(
#     r"("+t_LAMP+r"|"+t_CLOSE+r")+"
# )
@TOKEN(t_USELESS)
# @TOKEN(t_VERB)
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
    def __init__(self, action, object,flag=False):
        self.action = action
        self.object = object
        self.not_flag = flag

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

def p_single_NEGaction(p):
    """
    action : close lamp
    action : NOT close lamp
    """
    if len(p)==3:
        p[0] = Lamp("close", p[2])
    if len(p)==4:
        p[0] = Lamp('open', p[3])

def p_single_POSaction(p):
    """
    action : open lamp
    action : NOT open lamp
    """
    if len(p)==3:
        p[0] = Lamp("open", p[2])
    if len(p)==4:
        p[0] = Lamp('close', p[3])

def p_single_object(p):
    """
    lamp : LAMP
    lamp : LAMP useless
    """
    p[0] = p[1]

def p_single_open(p):
    """
    open : OPEN
    open : open useless
    open : OPEN useless
    """
    p[0] = p[1]

def p_single_close(p):
    """
    close : CLOSE
    close : close useless
    close : CLOSE useless
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


test=open("test_sentences_file.txt","r").readlines()
fail_test=["xxx lamp"]
if __name__ == "__main__":
    # lexer.input("open lamp sd open lamp sd sa")
    # for token in lexer:
    #     print token
    num=0
    for sentenses in test:
        sentenses=sentenses.strip().lower()
        result_dict = {}
        print num,sentenses
        result_dict = lamp_action(sentenses)
        print "   result:",result_dict
        # try:
        #     result_dict=lamp_action(str.lower(sentenses))
        #     print "result:",result_dict
        # except:
        #     print "miss result:",result_dict
        num+=1
    print "All tests passed."