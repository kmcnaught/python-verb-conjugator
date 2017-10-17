import argparse
import requests
from bs4 import BeautifulSoup


VERBIX_TABLE_URL = 'http://tools.verbix.com/webverbix/personal/template.htm'
VERBIX_LANG_CODES_URL = 'http://api.verbix.com/conjugator/html'
VERBIX_URL = 'http://api.verbix.com/conjugator/html?language={0}&tableurl=' \
              + VERBIX_TABLE_URL \
              + '&verb={1}'
VERBIX_CITATION = """
This tool uses the Verbix online conjugation API at http://www.verbix.com
The content extracted may be copied for non-commercial usage.
See http://www.verbix.com/webverbix/termsofuse.html
"""


def print_verbix_citation():
    """Necessary citation for Verbix
    """
    print(VERBIX_CITATION)


def verbix_connection_okay():
    """Test connection to verbix website
    """
    try:
        requests.get(VERBIX_TABLE_URL)
    except requests.exceptions.RequestException as e:  
        print("\nError connecting to Verbix API\n")
        print(e)
        return False
    return True


def get_conjugations(lang, verb):
    """Use the verbix API to return a list of all conjugations
    of a given verb/language combination

    :param str lang: Language code
    :param str verb: Verb to conjugate
    """

    # Make http request    
    try: 
        req = requests.get(VERBIX_URL.format(lang, verb))    
    except requests.exceptions.RequestException as e:
        print("Exception connecting to Verbix API")
        print(e)
        return set([])       
    html_string = req.text    
    
    # Parse response using beautiful soup
    soup = BeautifulSoup(html_string, "html5lib")
    regular_verbs = soup.findAll('span', attrs={"class" : "normal"})
    irregular_verbs = soup.findAll('span', attrs={"class" : "irregular"})
    
    # Extract verbs from HTML elements
    # Verbs are classed as "normal" or "irregular"
    # Any compound verbs get split into individual words
    all_verbs = set([]) 
    for html_elem in regular_verbs:
        for word in html_elem.string.split():
            all_verbs.add(word)
        
    for html_elem in irregular_verbs:
        for word in html_elem.string.split():
            all_verbs.add(word)
           
    return all_verbs

def main():

    # Parse command line inputs
    parser = get_parser()
    args = parser.parse_args()
    language = args.lang
    input_file = args.input
    output_file = args.output

    # Adhering to verbix terms of use...
    print_verbix_citation()

    # Check connection to Verbix 
    if not verbix_connection_okay():
        print('\nPlease check your connection and try again\n')
        return        
    
    # Read input verbs
    with open(input_file) as f:
        content = f.readlines()
    
    # Conjugate verbs one by one
    all_words = conjugate_verbs(content, language)# Output final conjugations

    # Print out in alphabetical order
    all_words = sorted(all_words)
    with open(output_file, 'a') as f:
        for word in all_words:
            f.write(word)
            f.write('\n')

    print('\nOutput saved in {}\n'.format(output_file))


def get_parser():
    parser = argparse.ArgumentParser(description='Conjugate a list of verbs.')
    parser.add_argument('-l', '--lang', type=str, required=True,
                        help="3-character language code. For language codes, see {}".format(VERBIX_LANG_CODES_URL))
    # TODO: single quotes
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='input file (list of infinitive verbs)')
    parser.add_argument('-o', '--output', type=str,
                        default="out.txt",
                        help='output file (list of conjugated verbs)')
    return parser


def conjugate_verbs(content, language):
    all_words = set([])
    for verb in content:
        print('Conjugating {}'.format(verb))
        words = get_conjugations(language, verb)
        if words:
            all_words.update(words)
        else:
            print('Error conjugating verb "{}" in language "{}"'.format(verb, language))

    return all_words


if __name__ == '__main__': main()

