import itertools
import re

import helpers
import err

REPLACEMENT_BUILTINS = {
    'True': 'true',
    'False': 'false',
    'None': 'none',
}
indent_level = 0

valid_funcname = re.compile(r'^[A-Za-z_]\w*$')
valid_attribute = re.compile(r'^([A-Za-z_]\w*\.)*[A-za-z_]\w*$')
valid_param_name = re.compile(
    r'^[A-Za-z_]\w*\=\'.*?\'$|^[A-Za-z_]\w*\=\".*?\"$|^[A-Za-z_]\w*\=[A-Za-z_]\w*$|'
    r'^[A-Za-z_]\w*\=\d+\.?\d*$|^[A-Za-z_]\w*\=\d*\.?\d+$|^\d+\.?\d*$|^\d*\.?\d+$|'
    r'^[A-Za-z_]\w*$|^\"[A-Za-z_]\w*\"$|^\'[A-Za-z_]\w*\'$'
)


def new_function(function_name, params, body, outfile):
    params_string = ', '.join(params)
    
    global indent_level
    func_definition_line = f"def {function_name}({params_string}):"
    helpers.write_indented_line(func_definition_line, outfile, indent_level)
    indent_level += 1
    transpile(body, outfile)
    indent_level -= 1


def find_and_validate_params(tokens, start_index, end_index):
    param_tokens = tokens[start_index+1:end_index]
    params = ''.join(param_tokens).split(',')
    params = [param.strip() for param in params]

    # Last trailing comma acceptable, so last param can be empty
    # If it is empty simply ignore it
    if not params[-1]:
        params.pop()
    
    for param in params:
        if not valid_param_name.match(param):
            error_msg = "Invalid parameter token"
            err._SyntaxError(error_msg, tokens, start_index)
    
    return params, end_index + 1


def find_closing_bracket(brackets, tokens, start_index):
    opening_bracket, closing_bracket = brackets
    open_count, close_count = 0, 0
    for index, token in enumerate(tokens[start_index:], start_index):
        if token == opening_bracket:
            open_count += 1
        elif token == closing_bracket:
            close_count += 1
        if close_count == open_count:
            return index
    
    error_msg = f"Expected '{closing_bracket}'"

    err._SyntaxError(error_msg, tokens, start_index)


def transpile(tokens, outfile):
    ti = 0
    while ti < len(tokens):
        if tokens[ti] == 'func':
            # Make sure next token is a valid function name
            if valid_funcname.match(tokens[ti+1]) == None:
                err._NameError(tokens, tokens[ti+1])
            function_name = tokens[ti+1]
            # Followed by parenthesis
            if tokens[ti+2] != '(':
                error_msg = "Expected '('"
                err._SyntaxError(error_msg, tokens, ti+2)

            opening_bracket_index = ti + 2
            closing_bracket_index = find_closing_bracket(
                '()', tokens, opening_bracket_index
            )
            
            # This call moves token index 1 ahead of the closing parenthesis
            params, ti = find_and_validate_params(
                tokens, opening_bracket_index, closing_bracket_index
            )

            while tokens[ti] == '\n':
                ti += 1

            if tokens[ti] != '{':
                error_msg = "Expected '{'"
                err._SyntaxError(error_msg, tokens, ti)

            opening_brace_index = ti
            closing_brace_index = find_closing_bracket(
                r'{}', tokens, opening_brace_index
            )
            body_start_index = opening_brace_index + 1
            body_end_index = closing_brace_index
            body = tokens[body_start_index:body_end_index]

            new_function(function_name, params, body, outfile)
            ti = body_end_index + 1
        elif re.match(valid_attribute, tokens[ti]):
            #TODO: super hacky
            line_start = ti
            line_end = helpers.find_next_occurance('\n', tokens, ti)

            line = ''.join(tokens[line_start:line_end])
            helpers.write_indented_line(line, outfile, indent_level)
            ti = line_end + 1
        elif tokens[ti] == '\n':
            ti += 1


def compile_ppp(file, outfile_name):
    lines = file.readlines()
    token_regex = re.compile(r'[\[\]\(\)\{\}\'\"\.\,\+\-\*\/\%\!\=\\]|\w+')
    tokenized_lines = [re.findall(token_regex, line) for line in lines]
    tokens = list(itertools.chain.from_iterable(([*line, '\n'] for line in tokenized_lines)))

    if not outfile_name:
        outfile_name = 'a'
    if '.' not in outfile_name:
        outfile_name += '.ppc'

    with open(outfile_name, 'w') as outfile:
        transpile(tokens, outfile)
    
    return outfile_name