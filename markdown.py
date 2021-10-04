import re
from typing import AnyStr


def parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False
    for line in lines:
        if re.match('###### (.*)', line):
            line = '<h6>' + line[7:] + '</h6>'
        elif re.match('## (.*)', line):
            line = '<h2>' + line[3:] + '</h2>'
        elif re.match('# (.*)', line):
            line = '<h1>' + line[2:] + '</h1>'

        line_starts_with_asterisk_regex_match = re.match(r'\* (.*)', line)  ####
        if line_starts_with_asterisk_regex_match and in_list:
            in_list = True
            check_and_add_emphasis = italicize
            list_item = format_list_item(check_and_add_emphasis, line_starts_with_asterisk_regex_match)
            new_i = list_item
        elif in_list:
            in_list_append = True
            in_list = False
            new_i = line
        elif line_starts_with_asterisk_regex_match:
            in_list = True

            check_and_add_emphasis = add_emphasis
            list_item = format_list_item(check_and_add_emphasis, line_starts_with_asterisk_regex_match)
            line = '<ul>' + list_item
            new_i = '<ul>' + list_item
        else:
            new_i = line  ####
        result = in_list, in_list_append, new_i
        in_list, in_list_append, new_i = result
        m = re.match('<h|<ul|<p|<li', new_i)
        if not m:
            new_i = '<p>' + new_i + '</p>'

        new_i = add_emphasis(new_i)
        if in_list_append:
            new_i = '</ul>' + new_i
            in_list_append = False
        res += new_i
    if in_list:
        res += '</ul>'
    return res


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
