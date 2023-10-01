import os
import json
from pathlib import Path
from pprint import pprint as pp


def h():
    a = input()
    i = int(input())

    if i:
        print('h')
        os.system(f'attrib +s +h {a}')
    else:
        print('r')
        os.system(f'attrib -s -h {a}')


def read_json():
    # parse values from json items
    collection = str(Path(__file__).resolve().parent / 'data/collection.json')
    encoding = 'utf-8'

    # Read the file with the specified encoding
    with open(collection, 'r', encoding=encoding) as file:
        json_data = file.read()
        jsn = json.loads(json_data)

    # get values, if value contains non empty lists
    words = []
    for i in jsn.values():
        if i:
            for word in i:
                words.append(word.split(':')[1]+'\n')

    words = set(words)
    with open(r'C:\Users\Burac\Desktop\-\RENEJR\back\downloads\python\P\Meme\main\modules\data\mainmodulesdata.txt','a') as f:
        f.writelines(words)


if __name__=='__main__':
    h()

    pass