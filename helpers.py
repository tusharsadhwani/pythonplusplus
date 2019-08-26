def get_line_number(tokens, token_index):
    line_number = 1
    for token in tokens[:token_index]:
        if token == '\n':
            line_number += 1
    
    return line_number


def find_next_occurance(_token, tokens, start_index):
    for index, token in enumerate(tokens[start_index:], start_index):
        if token == _token:
            return index
    return -1


def write_indented_line(line, outfile, indent_level):
    indent = '    ' * indent_level
    outfile.write(indent + line + '\n')