from helpers import get_line_number

def _NameError(tokens, token_index):
    line_number = get_line_number(tokens, token_index)
    print(f'NameError: Invalid name at line {line_number}')
    exit(1)

def _SyntaxError(error_msg, tokens, token_index):
    msg = 'SyntaxError: {} on line {}'
    line_number = get_line_number(tokens, token_index)
    print(msg.format(error_msg, line_number))
    exit(1)