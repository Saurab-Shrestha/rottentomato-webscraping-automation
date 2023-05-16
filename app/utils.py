import re

def remove_punctuations(string):
    pattern = r'[\"\',]'
    return re.sub(pattern, '', string)