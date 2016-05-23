#!/usr/bin/env python3
#
# This filter removes most HTML noise from wikipedia/xx/yyyymmdd.content.
# Author: Hao Tang, 2016-05-22

import sys
import json
import re

def count(text, c):
    return sum([1 if d == c else 0 for d in text])

def record_to_wiki(record):
    entry = json.loads(record)
    page = entry['data']['query']['pages']
    key = list(page.keys())[0]
    if 'revisions' in page[key]:
        return page[key]['revisions'][0]['*']
    else:
        return ''

def remove_quotes(text, start, end):
    # Remove anything within `start` and `end`, with nesting.

    result = ''
    stack = []
    text_start = 0
    i = 0

    while i < len(text):
        if text[i:].startswith(start):
            if len(stack) == 0:
                result += text[text_start:i]
            stack.append((start, i))
            i += len(start)
        elif text[i:].startswith(end):
            if len(stack) > 0:
                del stack[-1]
            if len(stack) == 0:
                text_start = i + len(end)
            i += len(end)
        else:
            i += 1

    result += text[text_start:]
    return result

def remove_links(text):
    # Remove MediaWiki's [[...]] links, like remove_quotes().

    start = '[['
    end = ']]'
    result = ''
    stack = []
    text_start = 0
    i = 0

    while i < len(text):
        if text[i:].startswith(start):
            if len(stack) == 0:
                result += text[text_start:i]
            stack.append((start, i))
            i += len(start)
        elif text[i:].startswith(end):
            if len(stack) == 0:
                print(text[i-50:i+20])
                exit()

            t = text[stack[-1][1] + len(start):i]

            if 'File:' not in t and 'Category:' not in t:
                c = count(t, '|')
                if c == 0:
                    result += t
                elif c == 1:
                    result += re.sub(r'.+?\|(.+?)', r'\1', t)
                else:
                    pass
            
            if len(stack) > 0:
                del stack[-1]
            if len(stack) == 0:
                text_start = i + len(end)
            i += len(end)
        else:
            i += 1

    return result

def parse_wiki(text):
    # Naive MediaWiki parser, one line at a time.
    lines = text.split('\n')
    i = 0
    docs = []
    while i < len(lines):
        if (re.match('= *.+ *=', lines[i])
                or re.match('== *.+ *==', lines[i])
                or re.match('=== *.+ *===', lines[i])
                or re.match('==== *.+ *====', lines[i])
                or re.match('====== *.+ *======', lines[i])):
            docs.append(('header', i, i+1))
        elif len(lines[i]) > 0 and lines[i][0] in '*#;:':
            docs.append(parse_list(lines, i))
        else:
            docs.append(parse_paragraph(lines, i))

        i = docs[-1][2]
    return docs

def parse_list(lines, i):
    k = i
    while i < len(lines) and len(lines[i]) > 0 and lines[i][0] in '*#;:':
        i += 1
    return ('list', k, i)

def parse_paragraph(lines, i):
    k = i
    while (i < len(lines) and lines[i] != ''
            and not lines[i][0] in '=*#;:'):
        i += 1
    while i < len(lines) and lines[i] == '':
        i += 1
    return ('par', k, i)

for line in sys.stdin:
    text = record_to_wiki(line)

    # Clean up text.  In this order, because different tags can nest.

    # Each step traverses the entire text.
    # Much faster would be to build a parse tree and traverse that instead.
    # To speed up even more, after that,
    # port to C++ with a JSON library and std::regex.

    text = remove_quotes(text, '{{', '}}')
    text = remove_quotes(text, '{|', '|}')
    text = remove_quotes(text, '<!--', '-->')

    text = remove_links(text)

    text = re.sub(r'\[.+? (.+?)\]', r'\1', text)

    text = re.sub('\'\'\'', '', text)
    text = re.sub('\'\'', '', text)
    text = re.sub(r'\[\[', '', text)
    text = re.sub(r'\]\]', '', text)

    text = remove_quotes(text, '<gallery>', '</gallery>')
    text = re.sub('<references *?/>', '', text)
    text = remove_quotes(text, '<ref', '</ref>')
    text = re.sub('<.+?>', '', text)

    text = re.sub('\n\n\n+', '\n\n', text)

    docs = parse_wiki(text)
    lines = text.split('\n')

    for d in docs:
        if d[0] == 'par':
            par = '\n'.join(lines[d[1]:d[2]])
            if par.strip() == '':
                continue
            print(par.strip())
