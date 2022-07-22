#!/usr/bin/python

import os
import re
from buddy_shared import AllOneRange


def get_packages_path():
    return os.path.join('packages')


def get_package_path(package_id):
    return os.path.join('packages', package_id + ".json")


def get_package_preview_path(package_id):
    return os.path.join('packages', package_id + ".png")


def get_package_image_path(package_id, file_index):
    return os.path.join('packages', package_id, str(file_index).zfill(4) + '.png')


def get_package_folder(package_id):
    return os.path.join('packages', package_id)


def is_package(package_id):
    return os.path.isfile(get_package_path(package_id))


def find_package_with_prefix(prefix):
    package_path = get_packages_path()
    for path in os.listdir(package_path):
        if os.path.isfile(os.path.join(package_path, path)):
            x = re.search("^[a-zA-z0-9_-]+\\.json$", path)
            if x != None and path.startswith(prefix):
                return path[0:-5]
    return None


def get_id_name(prompt):
    while True:
        user_input = input(f'{prompt}: ').lower()
        x = re.search("^[a-zA-z0-9_-]+$", user_input)
        if x == None:
            print('Invalid input')
        else:
            return user_input


def get_id_name_with_search(prompt):
    while True:
        user_input = input(f'{prompt}: ').lower()
        x = re.search("^[a-zA-z0-9_-]+[*]{0,1}$", user_input)
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

def get_float(prompt):
    while True:
        user_input = input(f'{prompt}: ').lower()
        try:
            return float(user_input)
        except ValueError:
            print('Invalid float, try again')


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
    user_input = input(f'{prompt}:([N]o|[Y]es) ').lower()
    return user_input == 'yes' or user_input == 'y'


def get_all_one_range(prompt):
    while True:
        user_input = input(f'{prompt}:([A]ll|[O]ne|[R]ange|[C]ancel) ').lower()
        if user_input == 'all' or user_input == 'a':
            return AllOneRange.ALL
        elif user_input == 'one' or user_input == 'o':
            return AllOneRange.ONE
        elif user_input == 'range' or user_input == 'r':
            return AllOneRange.RANGE
        elif user_input == 'cancel' or user_input == 'c':
            return AllOneRange.CANCEL


def get_all_one(prompt):
    while True:
        user_input = input(f'{prompt}:([A]ll|[O]ne|[C]ancel) ').lower()
        if user_input == 'all' or user_input == 'a':
            return AllOneRange.ALL
        elif user_input == 'one' or user_input == 'o':
            return AllOneRange.ONE
        elif user_input == 'cancel' or user_input == 'c':
            return AllOneRange.CANCEL
