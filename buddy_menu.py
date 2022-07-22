#!/usr/bin/python

import buddy_utilities
import re
import os
import buddy_work
import buddy_utilities
import buddy_packages
from buddy_shared import AllOneRange
import math

import json
from random import SystemRandom

import buddy_globals as gl
import shortcuts

###############################################################################
# Package Menu
###############################################################################


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
            package_queue(package_data)
        elif user_input == 'stop' or user_input == 's':
            return
        # elif user_input == 'quit' or user_input == 'q':
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
    count = buddy_utilities.get_number("How Many Images")
    print()
    print(f'Add {count} images to package?')
    if buddy_utilities.get_yes_no("Approve"):
        cryptogen = SystemRandom()
        for i in range(0, count):
            package_data["files"].append(
                {"seed": cryptogen.randrange(1000, 9999999)})
        buddy_packages.save_package(package_data)


def package_queue(package_data):
    choice = buddy_utilities.get_all_one_range('Which Files')
    if choice == AllOneRange.ALL:
        # All
        for i in range(0, len(package_data['files'])):
            buddy_work.queue_enhance(package_data, i)
    elif choice == AllOneRange.ONE:
        file_index = buddy_utilities.get_index(
            'While File 0 - ' + str(len(package_data['files'])))
        if file_index < len(package_data['files']):
            buddy_work.queue_enhance(package_data, file_index)
    elif choice == AllOneRange.RANGE:
        start_index = buddy_utilities.get_index(
            'Start Index 0 - ' + str(len(package_data['files']) - 1))
        end_index = buddy_utilities.get_index(
            'End Index 0 - ' + str(len(package_data['files']) - 1))
        if start_index < end_index and start_index != end_index and end_index < len(package_data['files']):
            for i in range(start_index, end_index + 1):
                buddy_work.queue_enhance(package_data, i)


def package_enhance(package_data):
    choice = buddy_utilities.get_all_one_range('Which Files')
    if choice == AllOneRange.ALL:
        # All
        for i in range(0, len(package_data['files'])):
            buddy_work.enhance_package_file(package_data, i)
    elif choice == AllOneRange.ONE:
        file_index = buddy_utilities.get_index(
            'While File 0 - ' + str(len(package_data['files'])))
        if file_index < len(package_data['files']):
            buddy_work.enhance_package_file(package_data, file_index)
    elif choice == AllOneRange.RANGE:
        start_index = buddy_utilities.get_index(
            'Start Index 0 - ' + str(len(package_data['files']) - 1))
        end_index = buddy_utilities.get_index(
            'End Index 0 - ' + str(len(package_data['files']) - 1))
        if start_index < end_index and start_index != end_index and end_index < len(package_data['files']):
            for i in range(start_index, end_index + 1):
                buddy_work.enhance_package_file(package_data, i)

###############################################################################
# Main Menu
###############################################################################


def list_packages():
    print()
    print('Package Listing')
    package_path = buddy_utilities.get_packages_path()

    for path in os.listdir(package_path):
        if os.path.isfile(os.path.join(package_path, path)):
            x = re.search("^[a-zA-z0-9_-]+\\.json$", path)
            if x != None:
                print(path)
    print()
    print('Queue Listing')
    for item in gl.runtime.WORK_QUEUE:
        package_id = item["package_id"]
        file_index = item['file_index']
        mode = item["mode"]
        print(f'{mode}: {package_id} - {file_index}')
    print()


def create_package():
    print()
    print('Create Package')
    package_id = buddy_utilities.get_id_name('Package Id')
    package_text = buddy_utilities.get_text('Text')

    print()
    print('Package Preview')
    print(f'Package ID: {package_id}')
    print(f'Text: {package_text}')
    if buddy_utilities.get_yes_no("Approval"):
        package_path = buddy_utilities.get_package_path(package_id)
        if os.path.exists(package_path):
            print(f'Package Id: {package_id} already exists, skipping')
            return
        payload = {"id": package_id, "text": package_text, "files": []}
        with open(package_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        os.makedirs(buddy_utilities.get_package_folder(package_id))
        print()
        print('Package Created')


def select_package():
    print()
    print('Select Package')
    package_id = buddy_utilities.get_id_name_with_search('Package Id')
    if package_id.endswith('*'):
        package_id = package_id[:-1]
        package_id = buddy_utilities.find_package_with_prefix(package_id)
        if package_id is None:
            return
        package_data = buddy_packages.load_package(package_id)
    else:
        if buddy_utilities.is_package(package_id) == False:
            print(f'Unknown Package: {package_id}')
            return
        package_data = buddy_packages.load_package(package_id)

    print()
    print('Package Selected')
    print('ID: ' + package_data['id'])
    print('TEXT: ' + package_data['text'])
    print("FILES: " + str(len(package_data['files'])))
    package_modify(package_data)


def preview_package():
    print()
    print('Package Previews')
    selection = buddy_utilities.get_all_one("Which Packages")

    packages = []

    if selection == AllOneRange.ALL:
        packages = buddy_packages.load_all_package()
    elif selection == AllOneRange.ONE:
        package_id = buddy_utilities.get_id_name_with_search('Package Id')
        if package_id.endswith('*'):
            package_id = package_id[:-1]
            package_id = buddy_utilities.find_package_with_prefix(package_id)
            if package_id is None:
                return
            packages.append(buddy_packages.load_package(package_id))
        else:
            if buddy_utilities.is_package(package_id) == False:
                print(f'Unknown Package: {package_id}')
                return
            packages.append(
                package_data=buddy_packages.load_package(package_id))
    else:
        return

    if len(packages) == 0:
        print()
        print('No previews, stopping')
        return

    print()
    print('Approve Previews')

    for i in packages:
        print(i['id'] + ' - ' + str(len(i['files'])))

    if buddy_utilities.get_yes_no("Go"):

        IMAGE_OFFSET = 5

        for i in packages:
            package_id = i['id']
            file_count = len(i['files'])
            columns = 3
            rows = math.floor(file_count / 3)
            if file_count % 3 != 0:
                rows += 1

            target_file = buddy_utilities.get_package_preview_path(package_id)

            shortcuts.make_image(
                target_file, (gl.runtime.WIDTH * columns) + (IMAGE_OFFSET * (columns + 1)), (gl.runtime.HEIGHT * rows) + (IMAGE_OFFSET * (rows + 1)))

            for i in range(0, file_count):
                column = i % 3
                row = math.floor(i / 3)
                shortcuts.insert_image(target_file, buddy_utilities.get_package_image_path(
                    package_id, i), (IMAGE_OFFSET + (column * (gl.runtime.WIDTH + IMAGE_OFFSET))), (IMAGE_OFFSET + (row * (gl.runtime.HEIGHT + IMAGE_OFFSET))))


def config_loop():

    while True:
        print()

        for item in gl.runtime.CONFIGURATIONS:
            item_value = gl.get_config_value(item.name)
            print(f'{item.name} = "{item_value}"')

        user_input = input('Action: ').lower()

        if user_input == 'set' or user_input == 's':
            config_set()
        elif user_input == 'revert' or user_input == 'r':
            config_reset()
        elif user_input == 'quit' or user_input == 'q':
            return
        else:
            print()
            print('Available Commands:')
            print('[S]ET: Change a value')
            print('[R]EVERT: Revert to to a default value')
            print('[Q]UIT: Stop working on this package')


def config_set():
    config_name = buddy_utilities.get_id_name('Config Name').upper()

    for item in gl.runtime.CONFIGURATIONS:
        if item.name == config_name:
            item_value = gl.get_config_value(item.name)
            print(f'Current Value: {item_value}')
            if item.type == gl.ConfigurationType.STRING:
                item_value = input('New Value')
                if item_value is None or len(item_value) == 0:
                    return
            if item.type == gl.ConfigurationType.INT:
                item_value = buddy_utilities.get_number('New Value')
                if item_value < item.minValue or item_value > item.maxValue:
                    print(
                        f'Value is out of the range {item.minValue} - {item.maxValue}')
                    return
            if item.type == gl.ConfigurationType.FLOAT:
                item_value = buddy_utilities.get_float('New Value')
                if item_value < item.minValue or item_value > item.maxValue:
                    print(
                        f'Value is out of the range {item.minValue} - {item.maxValue}')
                    return

            gl.set_config_value(item.name, item_value)

            gl.save_configuration()

            return
    print('Unknown Config Name')
    return


def config_reset():
    config_name = buddy_utilities.get_id_name('Config Name').upper()

    for item in gl.runtime.CONFIGURATIONS:
        if item.name == config_name:
            item_value = gl.get_config_value(item.name)
            print(
                f'Current Value: {item_value} - Default: {item.defaultValue}')

            if buddy_utilities.get_yes_no('Revert Value'):
                gl.set_config_value(item.name, item.defaultValue)
                gl.save_configuration()

            return
    print('Unknown Config Name')
    return


def main_loop():
    print('Render Buddy')

    while True:
        user_input = input('Command:').lower()

        if user_input == 'list' or user_input == 'l':
            list_packages()
        elif user_input == 'add' or user_input == 'a':
            create_package()
        elif user_input == 'config' or user_input == 'c':
            config_loop()
        elif user_input == 'preview' or user_input == 'p':
            preview_package()
        elif user_input == 'select' or user_input == 's':
            select_package()
        elif user_input == 'execute' or user_input == 'e':
            buddy_work.execute_queue()
        elif user_input == 'quit' or user_input == 'q':
            break
        else:
            print('Available Commands:')
            print('[L]IST: Packages and Queue')
            print('[A]DD: Add a new package')
            print('[C]ONFIG: change program options')
            print('[S]ELECT: Load a package for work')
            print('[P]REVIEWS: Generate previews for packages')
            print('[E]XECUTE: Execute the queued items')
            print('[Q]UIT:')
