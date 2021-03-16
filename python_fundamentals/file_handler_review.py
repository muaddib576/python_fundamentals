text_file = '/Users/Brian/code_projects/python_fundamentals/new_file.txt'
# text_file = './new_file.txt'


def file_write():
    with open(text_file, 'w') as fh:
        fh.write('Hellooooo\n')

def file_read():
    with open(text_file, 'r') as fh:
        contents = fh.read()
    print(contents)

# file_write()
file_read()




'''
Exercise:
1) ls recipes/blueberry-muffins.md
2) ls /users/guest/music
3) ls ../letter.doc
4) ls ~/pictures
'''