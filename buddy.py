#!/usr/bin/python

from enum import Enum
from pathlib import Path
import sys
import random
import shutil
import subprocess
import math
import re
import os
import os.path
import json
from random import SystemRandom

from shortcuts import enhance_image, gen_image
from shortcuts import make_image
from shortcuts import insert_image

class AllOneRange(Enum):
    ALL = 1
    ONE = 2
    RANGE = 3

LR = 0.1
OPTIMISER = "Adam"
MAX_ITERATIONS = 300
MODELNAME = 'coco'

work = []

def ehnance_package_file(package_data, file_index):
    filepath = get_package_image_path(package_data['id'], file_index)
    if os.path.isfile(filepath):
        print('Updating Image ' + filepath)
        gen_image(package_data['text'], OPTIMISER, package_data['files'][file_index]['seed'], MAX_ITERATIONS, MODELNAME, filepath, LR, filepath)
    else:
        print('Generating Image ' + filepath)
        gen_image(package_data['text'], OPTIMISER, package_data['files'][file_index]['seed'], MAX_ITERATIONS, MODELNAME, filepath, LR, None)

def get_packages_path():
    return os.path.join('packages')


def get_package_path(package_id):
    return os.path.join('packages',package_id + ".json")

def get_package_image_path(package_id, file_index):
    return os.path.join('packages',package_id, str(file_index).zfill(4) + '.png')

def get_package_folder(package_id):
    return os.path.join('packages',package_id)


def is_package(package_id):
    return os.path.isfile(get_package_path(package_id))

    
def load_package(package_id):
    with open(get_package_path(package_id), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_package(package_data):
    package_path = get_package_path(package_data['id'])
    with open(package_path, 'w', encoding='utf-8') as f:
            json.dump(package_data, f, ensure_ascii=False, indent=4)

def get_id_name(prompt):
    while True:
        user_input = input(f'{prompt}: ').lower()
        x = re.search("^[a-zA-z0-9_-]+$", user_input)
        if x == None:
            print('Invalid input')
        else:
            return user_input

def get_number(prompt):
    while True:
        user_input = input(f'{prompt}: ').lower()
        x = re.search("^[1-9][0-9]*$", user_input)
        if x == None:
            print('Invalid input, try again')
        else:
            return int(user_input)


def get_index(prompt):
    while True:
        user_input = input(f'{prompt}: ').lower()
        x = re.search("^[0-9]+$", user_input)
        if x == None:
            print('Invalid input, try again')
        else:
            return int(user_input)

def get_text(prompt):
    while True:
        user_input = input(f'{prompt}: ').lower()
        x = re.search("^[a-zA-z0-9_\\- \\.,\\|\\^]+$", user_input)
        if x == None:
            print('Invalid input')
        else:
            return user_input


def get_yes_no(prompt):
    user_input = input(f'{prompt}:[No] ').lower()
    return user_input == 'yes' or user_input == 'y'

def get_all_one_range(prompt):
    while True:
        user_input = input(f'{prompt}:[All|One|Range] ').lower()
        if user_input == 'all' or user_input == 'a':
            return AllOneRange.ALL      
        if user_input == 'one' or user_input == 'o':
            return AllOneRange.ONE  
        if user_input == 'range' or user_input == 'r':
            return AllOneRange.RANGE  

def list_packages():
    print()
    print('Package Listing')
    package_path = get_packages_path()

    filenames = os.listdir(package_path)
    
    for path in os.listdir(package_path):
        if os.path.isfile(os.path.join(package_path, path)):
            x = re.search("^[a-zA-z0-9_-]+\\.json$", path)
            if x != None:
                print(path)
    print()    


def create_package():
    print()
    print('Create Package')
    package_id = get_id_name('Package Id')
    package_text = get_text('Text')
    
    print()
    print('Package Preview')
    print(f'Package ID: {package_id}')
    print(f'Text: {package_text}')
    if get_yes_no("Approval"):
        package_path = get_package_path(package_id)
        if os.path.exists(package_path):
            print(f'Package Id: {package_id} already exists, skipping')
            return
        payload = {"id": package_id, "text": package_text, "files":[]}
        with open(package_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        os.makedirs(get_package_folder(package_id))
        print()
        print('Package Created')
    

def execute_work():
    print('Listing')    

def select_package():
    print()
    print('Select Package')
    package_id = get_id_name('Package Id')
    if is_package(package_id) == False:
        print(f'Unknown Package: {package_id}')
        return
    package_data = load_package(package_id)
    
    print()
    print('Package Selected')    
    print('ID: ' + package_data['id'])
    print('TEXT: ' + package_data['text'])
    print("FILES: " + str(len(package_data['files'])))
    package_modify(package_data)

def package_modify(package_data):

    while True:
        print()
        user_input = input('Package: ').lower()
        
        if user_input == 'add' or user_input == 'a':
            package_add(package_data)
        elif user_input == 'enhance' or user_input == 'e':
            package_enhance(package_data)
        elif user_input == 'reset' or user_input == 'r':
            pass
        elif user_input == 'info' or user_input == 'i':
            pass
        elif user_input == 'queue' or user_input == 'q':
            pass
        elif user_input == 'stop' or user_input == 's':
            return
        #elif user_input == 'quit' or user_input == 'q':
        #    break
        else:
            print()
            print('Available Commands:')
            print('[A]DD: Add a new image to generate')
            print('[I]NFO: Learn about the files')
            print('[E]NHANCE: Update a file to add more detail')
            print('[R]ESET: Erase the file for later generation')
            print('[Q]UEUE: Add changes to the Queue')
            print('[S]TOP: Stop working on this package')

def package_add(package_data):
    count = get_number("How Many Images")
    print()    
    print(f'Add {count} images to package?')
    if get_yes_no("Approve"):
        cryptogen = SystemRandom()
        for i in  range(0, count):
            package_data["files"].append({"seed":cryptogen.randrange(1000, 9999999)})
        save_package(package_data)

def package_enhance(package_data):
    choice = get_all_one_range('Which Files')
    if choice == AllOneRange.ALL:
        # All
        for i in range(0, len(package_data['files'])):
            ehnance_package_file(package_data, i)
    elif choice == AllOneRange.ONE:
        file_index = get_index('While File 0 - ' + str(len(package_data['files'])))
        if file_index < len(package_data['files']):
            ehnance_package_file(package_data, file_index)
    else:
        start_index = get_index('Start Index 0 - ' + str(len(package_data['files']) - 1))
        end_index = get_index('End Index 0 - ' + str(len(package_data['files']) - 1))
        if start_index < end_index and start_index != end_index and end_index < len(package_data['files']):
            for i in range(start_index, end_index + 1):
                ehnance_package_file(package_data, i)

def main(argv):
    print('Render Buddy')
   
    while True:
        user_input = input('Command:').lower()
        
        if user_input == 'list' or user_input == 'l':
            list_packages()
        elif user_input == 'add' or user_input == 'a':
            create_package()
        elif user_input == 'config' or user_input == 'c':
            pass
        elif user_input == 'select' or user_input == 's':
            select_package()
        elif user_input == 'execute' or user_input == 'e':
            execute_work()
        elif user_input == 'quit' or user_input == 'q':
            break
        else:
            print('Available Commands:')
            print('[L]IST:')
            print('[A]DD: Add a new package')
            print('[C]REATE:')
            print('[S]ELECT:')
            print('[E]XECUTE:')
            print('[Q]UIT:')
   
if __name__ == "__main__":
   main(sys.argv[1:])