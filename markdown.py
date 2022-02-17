import re
from collections import namedtuple
from typing import AnyStr

ParsedMarkdown = namedtuple("HTMLLine", "line needs_list_closure")


def parse(markdown):
    output = ParsedMarkdown("", False)

    for line in split_markdown_into_lines(markdown):
        output = parse_line(line, output)

    needs_list_closure = output.needs_list_closure
    line = output.line
    if needs_list_closure:
        line = close_list(line)
        output = ParsedMarkdown(line, needs_list_closure)
    else:
        pass

    output_line = output.line
    return output_line


def parse_line(line, output):
    line1 = parse_headers(line)
    line1 = handle_paragraphs(line1)
    last_line_was_in_a_list, new_line = handle_list(output.needs_list_closure, line1, add_emphasis)
    new_result = output.line + new_line
    output = ParsedMarkdown(new_result, last_line_was_in_a_list)
    return output


def close_list(result):
    result += '</ul>'
    return result


def split_markdown_into_lines(markdown):
    return markdown.split('\n')


def handle_list(in_list, new_line, post_process):
    line_starts_with_asterisk_regex_match = re.match(r'\* (.*)', new_line)
    if line_starts_with_asterisk_regex_match:
        match = line_starts_with_asterisk_regex_match.group(1)
        if in_list:
            new_line = add_emphasis(wrap_string_in_tag(italicize(match), 'li'))
        else:
            new_line = '<ul>' + add_emphasis(wrap_string_in_tag(match, 'li'))
        in_list = True
    if in_list and not line_starts_with_asterisk_regex_match:
        in_list = False
        new_line = '</ul>' + new_line
    return in_list, post_process(new_line)


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
