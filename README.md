# python-verb-conjugator
Uses the Verbix API (http://www.verbix.com/) to conjugate lists of verbs. This may be useful for generating dictionaries for predictive text applications.

For terms of use see: http://www.verbix.com/webverbix/termsofuse.html

# Requirements
This is a command-line python program which requires:
- python3
- pip install requests html5lib beautifulsoup4
- An internet connection

#  Usage
```bash
usage: conjugate.py [-h] -l LANG -i INPUT [-o OUTPUT]

Conjugate a list of verbs.

optional arguments:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  3-character language code. For language codes, see
                        http://api.verbix.com/conjugator/html
  -i INPUT, --input INPUT
                        input file (list of infinitive verbs)
  -o OUTPUT, --output OUTPUT
                        output file (list of conjugated verbs)
```

# Example
The repo comes packaged with a sample text file with some french words. To test:
```bash
python conjugate.py -i sample-french.txt -l fra -o out_french.txt
```

# Languages supported
The Verbix API (and hence this tool) supports over twenty different languages. To see the list of supported languages and their codes, see:
http://api.verbix.com/conjugator/html#LanguageCodes
