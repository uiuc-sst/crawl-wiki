# crawl-wiki
Webscrape text for making a word list and a language model suitable for Kaldi ASR.

To collect about 60 files named `wikipedia/*/yyyymmdd.txt`, run `crawl_wikipedia_all_lang`.

# Todo
Filter more, to be appropriate for pseudo-swahili ASR:
- Replace numbers with newlines.
- Cull lines with fewer than 3 words?

[Scrape](http://ruby.bastardsbook.com/chapters/web-scraping/) more than just the top page?  
