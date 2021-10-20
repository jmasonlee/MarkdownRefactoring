import re
from typing import AnyStr


def parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False
    list2 = ''
    for i, line in enumerate(lines):
        if re.match('###### (.*)', line):
            line = wrap_string_in_tag(line[7:], 'h6')
        elif re.match('## (.*)', line):
            line = wrap_string_in_tag(line[3:], 'h2')
        elif re.match('# (.*)', line):
            line = wrap_string_in_tag(line[2:], 'h1')

        line_starts_with_asterisk_regex_match = re.match(r'\* (.*)', line)

        list = ''
        new_line = line
        while line_starts_with_asterisk_regex_match:
            in_list, line_starts_with_asterisk_regex_match, list = method_name(i, in_list,
                                                                               line_starts_with_asterisk_regex_match,
                                                                               lines, list, list2)
            break
        #wrap list in ul
        if list:
            new_line = list

        if line_starts_with_asterisk_regex_match and in_list:
            pass
        elif in_list:
            in_list_append = True
            in_list = False
            list2 = ''

        m = re.match('<h|<ul|<p|<li', new_line)
        if not m:
            line = wrap_string_in_tag(new_line, 'p')
            new_line = line

        new_line = add_emphasis(new_line)
        if in_list_append:
            new_line = '</ul>' + new_line
            in_list_append = False
        res += new_line
    if in_list:
        res += '</ul>'
    return res


def method_name(i, in_list, line_starts_with_asterisk_regex_match, lines, list, list2):
    if in_list:
        line = wrap_string_in_tag(italicize(line_starts_with_asterisk_regex_match.group(1)), 'li')
        line = add_emphasis(line)
        list += line
        list2 += line
    else:
        in_list = True
        line = wrap_string_in_tag(line_starts_with_asterisk_regex_match.group(1), 'li')
        list_item = add_emphasis(line)
        list += '<ul>' + list_item
        list2 += '<ul>' + list_item
    my_i = i
    line_starts_with_asterisk_regex_match = re.match(r'\* (.*)', lines[my_i])
    return in_list, line_starts_with_asterisk_regex_match, list


def wrap_string_in_tag(string, tag):
    line = f'<{tag}>' + string + f'</{tag}>'
    return line


def add_emphasis(line) -> AnyStr:
    line = bold(line)
    line = italicize(line)

    return line


def italicize(line):
    return replace_markdown_with_html('</em>', line, '(.*)_(.*)_(.*)', '<em>')


def bold(line):
    return replace_markdown_with_html('</strong>', line, '(.*)__(.*)__(.*)', '<strong>')


def replace_markdown_with_html(ending_tag, line, pattern, tag):
    match = re.match(pattern, line)
    if match:
        line = match.group(1) + tag + match.group(2) + ending_tag + match.group(3)
    return line
