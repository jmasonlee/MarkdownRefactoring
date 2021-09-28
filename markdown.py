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

            m_4 = re.match('(.*)_(.*)_(.*)', curr1)
            if m_4:
                curr1 = m_4.group(1) + '<em>' + m_4.group(2) + '</em>' + m_4.group(3)

            line = '<li>' + curr1 + '</li>'
    else:
        if in_list:
            in_list_append = True
            in_list = False
        result = in_list, in_list_append, line
        in_list, in_list_append, line = result
    return line, in_list, in_list_append


def add_emphasis(curr1) -> AnyStr:
    m__ = re.match('(.*)__(.*)__(.*)', curr1)
    if m__:
        curr1 = m__.group(1) + '<strong>' + m__.group(2) + '</strong>' + m__.group(3)
    m__1 = re.match('(.*)_(.*)_(.*)', curr1)
    if m__1:
        curr1 = m__1.group(1) + '<em>' + m__1.group(2) + '</em>' + m__1.group(3)
    return curr1
