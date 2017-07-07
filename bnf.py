import ply.yacc as yacc

from lex import tokens

def p_instr(p):
    '''instr : store_instr
             | write_instr
             | noop_instr
             | crash_instr'''
    p[0] = p[1]

def p_register_term(p):
    '''term : '[' REGISTER_NAME ']' '''
    p[0] = p.parser.registers[p[2]]

def p_memory_term(p):
    '''term : '[' NUMBER ']' '''
    p[0] = p.memory[int(p[2])]

def p_number_term(p):
    '''term : NUMBER '''
    p[0] = int(p[1])

def p_value_expr_simple(p):
    '''value_expr : term'''
    p[0] = p[1]

def p_value_expr_operator(p):
    '''value_expr : value_expr '-' term
                  | value_expr '+' term'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    else:
        assert p[2] == '-'
        p[0] = p[1] - p[3]
    
def p_crash_instr(p):
    '''crash_instr : CRASH'''
    p[0] = ('crash',)

def p_noop_instr(p):
    '''noop_instr : NOOP'''
    p[0] = ('noop',)

def p_write_instr(p):
    '''write_instr : WRITE INSTR value_expr''' 
    p[0] = ('write', p[2], p[3])

def p_store_instr(p):
    '''store_instr : STORE value_expr REGISTER_NAME'''
    p[0] = ('store', p[2], p[3])

def get_parser():
    return yacc.yacc()