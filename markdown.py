import re
from typing import AnyStr


def close_list(in_list: bool) -> str:
    if in_list:
        return '</ul>'
    else:
        return ""


def parse(markdown):
    result = ''
    in_list = False
    for line in markdown.split('\n'):
        in_list, new_line = parse_line(in_list, line)
        result += new_line
    result += close_list(in_list)
    return result


def parse_line(in_list, line):
    new_line = parse_headers(line)
    line_starts_with_asterisk_regex_match = re.match(r'\* (.*)', new_line)
    if line_starts_with_asterisk_regex_match:
        match = line_starts_with_asterisk_regex_match.group(1)
        if in_list:
            new_line = add_emphasis(wrap_string_in_tag(italicize(match), 'li'))
        else:
            new_line = '<ul>' + add_emphasis(wrap_string_in_tag(match, 'li'))
        in_list = True
    starts_with_tag = re.match('<h|<ul|<p|<li', new_line)
    if not starts_with_tag:
        new_line = wrap_string_in_tag(new_line, 'p')
    if in_list and not line_starts_with_asterisk_regex_match:
        in_list = False
        new_line = '</ul>' + new_line
    new_line = add_emphasis(new_line)
    return in_list, new_line


def parse_headers(line: str) -> str:
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
