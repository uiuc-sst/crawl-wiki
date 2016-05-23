#!/usr/bin/env python3
#
# Author: Hao Tang, 2016-05-22

import urllib.request
import sys
import time
import json

def popular_words(lang):
    # Return json string of a list of popular words in the specified language.
    res = urllib.request.urlopen('http://apifree.forvo.com/key/4c698823e6580210e815b7efc62ba316/'
        'format/json/action/popular-pronounced-words/language/{}'.format(lang))
    return res.read().decode('utf-8')

def word_pronunciations(word, lang):
    # Return a list of urls pointing to the pronunciations of a word.
    res = urllib.request.urlopen('http://apifree.forvo.com/key/4c698823e6580210e815b7efc62ba316/'
        'format/json/action/word-pronunciations/word/{}/language/{}'.format(
        urllib.parse.quote_plus(word), lang))
    return res.read().decode('utf-8')

if __name__ == '__main__':
    lang = sys.argv[1]
    words_data = popular_words(lang);

    for i in json.loads(words_data)['items']:
        prons_data = word_pronunciations(i['word'], lang)
        print(pros_data)
        for j in json.loads(prons_data)['items']:
            mp3_res = urllib.request.urlopen(j['pathmp3'])
            f = open('forvo/{}/{}.mp3'.format(lang, j['id']), 'wb')
            f.write(mp3_res.read())
            f.close()
            time.sleep(180)
