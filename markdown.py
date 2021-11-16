import re
from typing import AnyStr


def parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False
    for i, line in enumerate(lines):
        line = header_things(line)

        new_line = line
        line_starts_with_asterisk_regex_match = re.match(r'\* (.*)', line)

        if line_starts_with_asterisk_regex_match:
            if in_list:
                new_line = add_emphasis(wrap_string_in_tag(italicize(line_starts_with_asterisk_regex_match.group(1)), 'li'))
            else:
                in_list = True
                new_line = wrap_string_in_tag(line_starts_with_asterisk_regex_match.group(1), 'li')
                list_item = add_emphasis(new_line)
                new_line = '<ul>' + list_item

        if line_starts_with_asterisk_regex_match and in_list:
            pass
        elif in_list:
            in_list_append = True
            in_list = False

        starts_with_tag = re.match('<h|<ul|<p|<li', new_line)
        if not starts_with_tag:
            new_line = wrap_string_in_tag(new_line, 'p')

        if in_list_append:
            new_line = '</ul>' + new_line
            in_list_append = False
        res += add_emphasis(new_line)
    if in_list:
        res += '</ul>'
    return res


def header_things(line: str) -> str:
    if re.match('###### (.*)', line):
        line = wrap_string_in_tag(line[7:], 'h6')
    elif re.match('## (.*)', line):
        line = wrap_string_in_tag(line[3:], 'h2')
    elif re.match('# (.*)', line):
        line = wrap_string_in_tag(line[2:], 'h1')
    return line


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
