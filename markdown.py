import re
from collections import namedtuple
from typing import AnyStr

ParsedMarkdown = namedtuple("HTMLLine", "line needs_list_closure")


def parse(markdown):
    output = ParsedMarkdown("", False)

    for line in split_markdown_into_lines(markdown):
        last_line_was_in_a_list, line = parse_line(line, output)
        new_result = output.line + line
        output = ParsedMarkdown(new_result, last_line_was_in_a_list)
        output = output

    return close_list(output.line) if output.needs_list_closure else output.line


def parse_line(line, output):
    line = parse_headers(line)
    line = handle_paragraphs(line)
    last_line_was_in_a_list, line = handle_list(output.needs_list_closure, line, add_emphasis)
    return last_line_was_in_a_list, line


def close_list(result):
    result += '</ul>'
    return result


def split_markdown_into_lines(markdown):
    return markdown.split('\n')


def handle_list(in_list, new_line, post_process):
    line_starts_with_asterisk_regex_match = re.match(r'\* (.*)', new_line)
    is_list_item = bool(line_starts_with_asterisk_regex_match)
    new_line = start_list(in_list, new_line) if is_list_item else new_line
    if is_list_item:
        list_item = line_starts_with_asterisk_regex_match.group(1)
        new_line = start_list(in_list, new_line)
        if in_list:
            list_item = italicize(list_item)

        new_line += add_emphasis(wrap_string_in_tag(list_item, 'li'))
        in_list = True
    if in_list and not line_starts_with_asterisk_regex_match:
        in_list = False
        new_line = '</ul>' + new_line
    return in_list, post_process(new_line)


def start_list(in_list, new_line):
    if in_list:
        new_line = ""
    else:
        new_line = '<ul>'
    return new_line


def handle_paragraphs(new_line):
    starts_with_tag = re.match('^<h|<ul|<p|<li|\*', new_line)
    if not starts_with_tag:
        new_line = wrap_string_in_tag(new_line, 'p')
    return new_line


def parse_headers(line: str) -> str:
    if re.match('###### (.*)', line):
        line = wrap_string_in_tag(line[7:], 'h6')
    elif re.match('## (.*)', line):
        line = wrap_string_in_tag(line[3:], 'h2')
    elif re.match('# (.*)', line):
        line = wrap_string_in_tag(line[2:], 'h1')
    return line


def wrap_string_in_tag(string, tag):
    return f'<{tag}>' + string + f'</{tag}>'


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
