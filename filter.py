#!/bin/env python3
import requests
import json

class Filter:

    '''
    check for bad words in lines
    checker --> offline method
    api_filter --> online method
    '''
    API_KEY = "mg98jTx9n77KTfxHtdNQz2ByOHDPKY8M"
    wordlist = None
    line = None
    param = None

    def __init__(self, param, line, wordlist='./cursewords.txt'):
        self.wordlist = wordlist
        self.line = line
        self.param = param

    def checker(self, line, wordlist):
        with open(wordlist, 'r') as wordlistfd:
            words = wordlistfd.readlines()
            for word in words:
                templist1 = word.split()
                templist2 = line.split()
                for i in range(len(templist2)):
                    temp2 = templist2[i].lower()
                    if(temp2 == 'of' or temp2 == 'to' or temp2 == 'the' or temp2 == 'a' or temp2 == 'an' or temp2 == 'off' or temp2 == 'you' or temp2 == 'son'):
                        continue
                    for j in range(len(templist1)):
                        if(temp2 == templist1[j].lower()):
                            return temp2
        return False
    
    def api_filter(self, line):
        _header = {
                'apikey' : self.API_KEY
                  }
        _data = line
        _url = 'https://api.apilayer.com/bad_words?censor_character=*'
        r = requests.post(url=_url, data=_data, headers=_header)
        json_text = json.loads(r.text)
        if(int(json_text['bad_words_total'])):
           return json_text['content']
        return False
    
    def handle(self, param, line, wordlist):
        param = self.param
        if(param == 1):
            return self.checker(self.line, self.wordlist)
        elif(param == 0):
            return self.api_filter(line)
        else:
            raise Exception('method not found!')

if(__name__ == "__main__"):
    while True:
        filter = Filter()
        content, count_bad = filter.api_filter(input('q: '))
        print(content, count_bad)
