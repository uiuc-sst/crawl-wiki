#!/usr/bin/env python3
#
# Creates file forvo-lang or sbs-forvo-lang or sbs-wikipedia-lang-code?
# Author: Hao Tang, 2016-05-22

import sys

sbs_lang = []
f = open(sys.argv[1])
for line in f:
    sbs_lang.append(line.strip())
f.close()

wikipedia_lang = {}
f = open(sys.argv[2])
for line in f:
    parts = line.split('\t')
    wikipedia_lang[parts[0].strip()] = parts[2].strip()
f.close()

for ell in sbs_lang:
    if ell in wikipedia_lang:
        print('{}\t{}'.format(ell, wikipedia_lang[ell]))
    else:
        print(ell)
