#!/usr/bin/env python3
#
# Author: Hao Tang, 2016-05-22

import sys
import urllib.request
import urllib.parse
import json
import re
import datetime
import time

def query_page(title, lang):
    '''
    Return a JSON string fetched from wikipedia.
    title is the page title to fetch written in the specified language.
    lang is the language code from http://meta.wikimedia.org/wiki/List_of_Wikipedias.

    For example, to query the English language in English or in Spanish:
        query_page('English_language', 'en')
        query_page('Idioma_inglés', 'es')
    '''
    if '%' not in title:
        title = urllib.parse.quote_plus(title)

    query = (u'http://{}.wikipedia.org/w/api.php?format=json&action=query&titles={}'
        '&prop=revisions&rvprop=content&redirects').format(lang, title)
    res = urllib.request.urlopen(query)
    raw = res.read()
    return raw.decode('utf-8')


def titles_on_main(lang):
    # Return a list of titles from the main page with language code 'lang'.
    res = urllib.request.urlopen('http://{}.wikipedia.org/'.format(lang))
    raw = res.read()
    return [p for p in re.findall('href="/wiki/(.+?)"', raw.decode('utf-8'))
        if ':' not in p]

if __name__ == '__main__':
    lang = sys.argv[1]
    
    titles = titles_on_main(lang)
    
    for t in sorted(set(titles)):
        content = query_page(t, lang)
        if '"-1"' not in content:
            data = json.loads(content)
            print(json.dumps({'title': t, 'datetime': datetime.datetime.now().isoformat(), 'data': data}))
            print('ok: {} {}'.format(lang, t), file=sys.stderr)
        else:
            print('error: {} {}'.format(lang, t), file=sys.stderr)
    
        time.sleep(5)
