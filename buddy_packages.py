#!/usr/bin/python

from unittest import result
import buddy_utilities
import json
import os
import re


def list_package_ids():
    package_path = buddy_utilities.get_packages_path()

    results = []
    for path in os.listdir(package_path):
        if os.path.isfile(os.path.join(package_path, path)):
            x = re.search("^[a-zA-z0-9_-]+\\.json$", path)
            if x != None:
                results.append(path[0:-5])
    return results


def load_all_package():
    results = []
    for i in list_package_ids():
        results.append(load_package(i))
    return results


def load_package(package_id):
    with open(buddy_utilities.get_package_path(package_id), 'r', encoding='utf-8') as f:
        return json.load(f)


def save_package(package_data):
    package_path = buddy_utilities.get_package_path(package_data['id'])
    with open(package_path, 'w', encoding='utf-8') as f:
        json.dump(package_data, f, ensure_ascii=False, indent=4)
