from py_console import console

def checker(line, wordlist):
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
                        console.warn("someone abused: "+temp2)
                        return temp2
    return False

