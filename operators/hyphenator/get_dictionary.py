import os

def get_dictionary(dic_path=None):
    """Collect the words from the default dictionary"""
    
    if dic_path == None:
        addon_path = os.path.dirname(__file__)
        dic_path = os.path.join(addon_path, 'default_dictionary.txt')
    
    dictionary = {}
    
    f = open(dic_path, 'r')
    lines = f.readlines()
    f.close()
    
    for line in lines:
        word = line.rstrip().replace(' ', '')
        dictionary[word] = line.rstrip()
    
    return dictionary
