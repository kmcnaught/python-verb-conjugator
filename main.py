import argparse
import requests
from html.parser import HTMLParser

VERBIX_TABLE_URL = "http://tools.verbix.com/webverbix/personal/template.htm" 
VERBIX_URL = "http://api.verbix.com/conjugator/html?language={0}&tableurl=" \
              + VERBIX_TABLE_URL \
              + "&verb={1}"

def element_in_list_of_tuples(the_list, elem):    
    for item in the_list:
        if elem in item:
            return True
    return False

# Extract any pronouns and conjugated verbs from a verbix
# conjugation table.
# Both pronouns and verbs are the only things in "span" elements.
class ConjugationTableParser(HTMLParser):
    
    def __init__(self, ignore_pronouns=False):
        HTMLParser.__init__(self)
        self.relevant_tag = False
        self.data = set([]) 
        self.ignore_pronouns = ignore_pronouns        
    
    def handle_starttag(self, tag, attrs):
        if (tag == "span"):                     
            is_pronoun = element_in_list_of_tuples(attrs, 'pronoun');
            if not is_pronoun or not self.ignore_pronouns:                
                self.relevant_tag = True;

    def handle_endtag(self, tag):
        self.relevant_tag = False;
        
    def handle_data(self, data):
        if self.relevant_tag:
            for word in data.split():
                self.data.add(word)
        

def get_conjugations(lang, verb, ignore_pronouns):        
    r = requests.get(VERBIX_URL.format(lang, verb))
    parser = ConjugationTableParser(ignore_pronouns)
    parser.feed(r.text)
    if len(parser.data) == 0:
#         print("ERROR: {}".format(r.text))
        return None
    else:
        return parser.data

def main():

    # Parse command line inputs
    parser = argparse.ArgumentParser(description='Conjugate a list of verbs.')
    parser.add_argument('-l', '--lang', type=str, required=True,
                        help="3-character language code. For language codes, see http://api.verbix.com/conjugator/html")
    parser.add_argument('-i', '--input', type=str, required=True,
                       help='input file (list of infinitive verbs)')    
    parser.add_argument('-o', '--output', type=str,
                       default="out.txt",
                       help='output file (list of conjugated verbs)')
    parser.add_argument('--ignore-pronouns', action="store_true",
                        default=False)
    args = parser.parse_args()
    language = args.lang
    input_file = args.input
    output_file = args.output
    ignore_pronouns = args.ignore_pronouns
    
    # Read input varbs    
    with open(input_file) as f:
        content = f.read().splitlines()
    
    # Conjugate verbs one by one
    all_words = set([])     
    for verb in content:
        print('Conjugating {0}'.format(verb))
        words = get_conjugations(language, verb, ignore_pronouns)
        if words is not None:
            all_words.update(words)
        else:
            print("Error conjugating verb [{}] in language [{}]".format(verb, language))            

    # Output final conjugations 
    all_words = sorted(all_words)   
    with open(output_file, 'a') as f:
        for word in all_words:
            f.write(word)
            f.write('\n')


if __name__ == "__main__": main()