import ply.lex as lex
tokens = (
    'INSTR',
    'CRASH',
    'NOOP',
    'WRITE',
    'STORE',
    'NUMBER',
    'REGISTER_NAME',
)

def t_INSTR(t):
    r'\([^\s]+\)'
    t.value = t.value.strip('()')
    return t

t_CRASH = 'crash'
t_NOOP = 'noop'
t_WRITE = 'write'
t_STORE = 'store'
t_NUMBER = r'[0-9]+'
t_REGISTER_NAME = r'[abi]'

t_ignore = ' '

literals = [ '[', ']', '+', '-' ]

lexer = lex.lex()
