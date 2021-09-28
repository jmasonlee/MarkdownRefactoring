import re
from typing import AnyStr


def parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False
    for i in lines:
        if re.match('###### (.*)', i) is not None:
            i = '<h6>' + i[7:] + '</h6>'
        elif re.match('## (.*)', i) is not None:
            i = '<h2>' + i[3:] + '</h2>'
        elif re.match('# (.*)', i) is not None:
            i = '<h1>' + i[2:] + '</h1>'
        i, in_list, in_list_append = handle_lists(i, in_list, in_list_append)

        m = re.match('<h|<ul|<p|<li', i)
        if not m:
            i = '<p>' + i + '</p>'
        i = add_emphasis(i)
        if in_list_append:
            i = '</ul>' + i
            in_list_append = False
        res += i
    if in_list:
        res += '</ul>'
    return res


def handle_lists(line, in_list, in_list_append):
    line_starts_with_asterisk_regex_match = re.match(r'\* (.*)', line)
    if line_starts_with_asterisk_regex_match:
        if not in_list:
            in_list = True
            curr1 = line_starts_with_asterisk_regex_match.group(1)

            curr1 = add_emphasis(curr1)

            line = '<ul>'+'<li>' + curr1 + '</li>'
        else:
            curr1 = line_starts_with_asterisk_regex_match.group(1)

            curr1 = italicize(curr1)

            line = '<li>' + curr1 + '</li>'
    else:
        if in_list:
            in_list_append = True
            in_list = False
    return line, in_list, in_list_append


def italicize(line):
    emphasis_pattern = '(.*)_(.*)_(.*)'
    line_with_italics = re.match(emphasis_pattern, line)
    if line_with_italics:
        emphasis_tag = '<em>'
        ending_tag = '</em>'
        line = line_with_italics.group(1) + emphasis_tag + line_with_italics.group(2) + ending_tag + line_with_italics.group(3)
    return line


def add_emphasis(curr1) -> AnyStr:
    ###
    emphasis_pattern = '(.*)__(.*)__(.*)'
    emphasis_tag = '<strong>'
    ending_tag = '</strong>'
    m__ = re.match(emphasis_pattern, curr1)
    if m__:
        curr1 = m__.group(1) + emphasis_tag + m__.group(2) + ending_tag + m__.group(3)
    ###
    ###
    emphasis_pattern = '(.*)_(.*)_(.*)'
    emphasis_tag = '<em>'
    ending_tag = '</em>'
    m__ = re.match(emphasis_pattern, curr1)
    if m__:
        curr1 = m__.group(1) + emphasis_tag + m__.group(2) + ending_tag + m__.group(3)
    ###
    return curr1
