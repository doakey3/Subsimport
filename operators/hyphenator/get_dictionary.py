import os

def get_dictionary(dic_path=None, lang='en-us'):
    """Collect the words from the default dictionary"""

    if dic_path == None:
        module_path = os.path.dirname(__file__)
        dic_path = os.path.join(module_path, 'dictionaries', lang + '.txt')

    dictionary = {}

    try:
        f = open(dic_path, 'r')
        lines = f.readlines()
        f.close()

        for line in lines:
            word = line.rstrip().replace(' ', '')
            dictionary[word] = line.rstrip()

    except FileNotFoundError:
        dictionary = {}

    return dictionary