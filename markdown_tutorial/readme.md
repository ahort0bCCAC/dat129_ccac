# JSON Processing
JSON is a data interchange format used widely on the internet and supported by most pogramming languages in wide use today.

## Encoding python objects in JSON
'''

textBooks = {}
textBooks["Text Books"]=['Intro to Python', 'Statistics Unlocking the Power of Data', 'Python for Evervybody',
                         'Database Design 2nd Edition', 'Pro Git' ]
...
with open('textBooks.json', 'w') as textBooks_file:
    textBooks_file.write(json.dumps(textBooks))
'''
