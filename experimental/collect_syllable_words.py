"""
This is a module I used to collect words for my default dictionary.
I pinged 3 different online dictionaries to search for words
"""

from bs4 import BeautifulSoup
import urllib.request

count_dictionary = {}
f = open('cleaned.txt', 'r')
lines = f.readlines()
f.close()
for i in range(len(lines)):
    if not lines[i].rstrip() == '':
        word = lines[i].split(' ')[0]
        count = int(lines[i].split(' ')[1].rstrip())
        count_dictionary[word] = count
        
words = list(sorted(count_dictionary.keys()))

for i in reversed(range(len(words))):
    try:
        print('Trying: ' + words[i])
        url = "http://www.dictionary.com/browse/" + words[i]
        data = urllib.request.urlopen(url, timeout=3).read()
        soup = BeautifulSoup(data, 'html.parser')
        tag = soup.find("span", {"class" : "me"})
        word = tag['data-syllable']
        word = word.replace('·', ' ').lower()
        if word.replace(' ', '') == words[i]:
            print("RECIEVED: " + word)
            dictionary3 = open('dictionary3.txt', 'a')
            dictionary3.write(word + '\n')
            dictionary3.close()
        else:
            raise IndexError
    
    except:
        
        try:
            print('Retrying: ' + words[i])
            url = "http://www.syllablecount.com/syllables/" + words[i]
            data = urllib.request.urlopen(url, timeout=3).read()
            soup = BeautifulSoup(data, 'html.parser')
            word = soup.findAll("p", {"id" : "ctl00_ContentPane_paragraphtext2"})[0].text.split(' ')[-1].strip().replace('-', ' ').lower()
            print("RECIEVED: " + word)
            dictionary3 = open('dictionary3.txt', 'a')
            dictionary3.write(word + '\n')
            dictionary3.close()
        
        except:
            try:
                print("Reretrying: " + words[i])
                url = 'https://www.howmanysyllables.com/words/' + words[i]
                data = urllib.request.urlopen(url, timeout=3).read()
                soup = BeautifulSoup(data, 'html.parser')
                word = soup.findAll("span", {"class" : "no_b"})[0].text.replace('-', ' ').lower()
                print("RECIEVED: " + word)
                dictionary3 = open('dictionary3.txt', 'a')
                dictionary3.write(word + '\n')
                dictionary3.close()
            
            except:
                failures = open('failures.txt', 'a')
                failures.write(words[i] + '\n')
                failures.close()
        
