import argparse as ag
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init
init()

parser = ag.ArgumentParser()
parser.add_argument('directory')
args = parser.parse_args()

# Directory creation
try:
    os.mkdir(args.directory)
except FileExistsError:
    pass


history = deque()
choice = input()
last = ''
while choice != 'exit':
    if choice == 'back':
        if history:
            print(Fore.BLUE + history.pop())
        choice = input()
        continue
    if choice in os.listdir(args.directory):

        with open(args.directory + '/' + choice) as file:
            print(file.read())
            if last:
                history.append(last)
            last = file.read()
    elif '.' in choice:
        try:
            r = requests.get(r'https://' + choice)
        except requests.exceptions.ConnectionError:
            print('Incorrect URL')
            continue
        if r:
            soup = BeautifulSoup(r.content, 'html.parser')
            new=[]
            for i in soup.find_all():
                if i.name == 'a':
                    new.append(Fore.BLUE + i.text)
                else:
                    new.append(i.text)
            soup = '\n'.join(new)
            print(soup)
            with open(args.directory + '/' + '.'.join(choice.split('.')[:-1]), 'w', encoding='UTF-8') as file:
                file.write(soup)
            if last:
                history.append(soup)
            last = soup
        else:
            print('Error: Incorrect URL')
    else:
        print('Incorrect URL')
    choice = input()
