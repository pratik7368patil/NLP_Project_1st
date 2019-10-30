text = "To be or not to be"
_data = text.split(' ')
_data_lower = set([w.lower() for w in _data])
print(len(_data_lower))

text5 = 'ouagadougou'
text6 = text5.split('ou')
print(text6)
data = 'ou'.join(text6)
print(data)

f = open('data_file.txt', 'r')
text10 = f.read()
text11 = text10.splitlines()
text12 = text11[0].split(' ')
print(text12)
text13 = ''.join(text12)
print(text13)

tweet = "@nltk Text analysis is awesome! #regex #pandas #python"
re_exp = tweet.split(' ')
print([w for w in re_exp if w.startswith('#')])

# read file and fetch all dates from it using regular expression.
import re

dates_with_number_in_file = re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', text10)
print(dates_with_number_in_file)
dates_with_spell_in_file = re.findall(r'(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (?:\d{1,2}, )?\d{4}', text10)
print(dates_with_spell_in_file)

