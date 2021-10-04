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
    if in_list:
        if line_starts_with_asterisk_regex_match:
            check_and_add_emphasis = italicize
            list_item = format_list_item(check_and_add_emphasis, line_starts_with_asterisk_regex_match)
            line = list_item
        else:
            in_list_append = True
            in_list = False
    else:
        if line_starts_with_asterisk_regex_match:  ####
            in_list = True
            emphasis = add_emphasis
            item = format_list_item(emphasis, line_starts_with_asterisk_regex_match)
            line = '<ul>' + item

    return line, in_list, in_list_append


def format_list_item(check_and_add_emphasis, line_starts_with_asterisk_regex_match):
    curr1 = line_starts_with_asterisk_regex_match.group(1)
    curr1 = check_and_add_emphasis(curr1)
    list_item = '<li>' + curr1 + '</li>'
    return list_item


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
