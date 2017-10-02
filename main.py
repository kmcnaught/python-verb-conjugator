import argparse
import requests
from bs4 import BeautifulSoup

VERBIX_TABLE_URL = "http://tools.verbix.com/webverbix/personal/template.htm" 
VERBIX_URL = "http://api.verbix.com/conjugator/html?language={0}&tableurl=" \
              + VERBIX_TABLE_URL \
              + "&verb={1}"
      
# Test connection to verbix website  
def verbix_connection_okay():
    try: 
        req = requests.get(VERBIX_TABLE_URL)    
    except requests.exceptions.RequestException as e:  
        print("\nError connecting to Verbix API\n")
        print(e)
        return False
    return True

def get_conjugations(lang, verb):        
    
    # Make http request    
    try: 
        req = requests.get(VERBIX_URL.format(lang, verb))    
    except requests.exceptions.RequestException as e:  
        print("Exception connecting to Verbix API")
        return None      
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
    parser = argparse.ArgumentParser(description='Conjugate a list of verbs.')
    parser.add_argument('-l', '--lang', type=str, required=True,
                        help="3-character language code. For language codes, see http://api.verbix.com/conjugator/html")
    parser.add_argument('-i', '--input', type=str, required=True,
                       help='input file (list of infinitive verbs)')    
    parser.add_argument('-o', '--output', type=str,
                       default="out.txt",
                       help='output file (list of conjugated verbs)')
    args = parser.parse_args()
    language = args.lang
    input_file = args.input
    output_file = args.output

    # Check connection to Verbix 
    if not verbix_connection_okay():
        print("\nPlease check your connection and try again\n")
        return        
    
    # Read input varbs    
    with open(input_file) as f:
        content = f.read().splitlines()
    
    # Conjugate verbs one by one
    all_words = set([])     
    for verb in content:
        print('Conjugating {0}'.format(verb))
        words = get_conjugations(language, verb)
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