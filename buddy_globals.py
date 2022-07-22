#!/usr/bin/python

from enum import Enum
import os
import json
from re import L


class runtime:
    LR = 0.1
    OPTIMISER = "Adam"
    MAX_ITERATIONS = 300
    START_ITERATIONS = 400
    UPDATE_ITERATIONS = 300
    WIDTH = 300
    HEIGHT = 300
    MODALNAME = 'coco'
    WORK_QUEUE = []
    CONFIGURATIONS = []


class ConfigurationType(Enum):
    INT = 1
    STRING = 2
    FLOAT = 3


class BuddyConfiguration:
    name = ''
    display = ''
    type = ConfigurationType.STRING
    minValue = None
    maxValue = None
    defaultValue = None

    def __init__(self, name, display, type, minValue, maxValue, defaultValue):
        self.name = name
        self.display = display
        self.type = type
        self.minValue = minValue
        self.maxValue = maxValue
        self.defaultValue = defaultValue


def get_configuration():
    results = []

    results.append(BuddyConfiguration("WIDTH", "Output Width",
                   ConfigurationType.INT, 16, 4096, 256))
    results.append(BuddyConfiguration("HEIGHT", "Output Height",
                   ConfigurationType.INT, 16, 4096, 256))
    results.append(BuddyConfiguration("UPDATE_ITERATIONS",
                   "Update Iterations", ConfigurationType.INT, 1, 2000, 200))
    results.append(BuddyConfiguration("START_ITERATIONS",
                   "Start Iterations", ConfigurationType.INT, 1, 2000, 300))
    results.append(BuddyConfiguration("MODALNAME", "Modal Name",
                   ConfigurationType.STRING, "", "", "vqgan_imagenet_f16_16384"))
    results.append(BuddyConfiguration("OPTIMISER", "Optimiser",
                   ConfigurationType.STRING, "", "", "Adam"))
    results.append(BuddyConfiguration("LR", "Learning Rate",
                   ConfigurationType.FLOAT, 0.01, 1.00, 0.1))

    return results


def save_configuration():

    json_file = {"LR": runtime.LR, "OPTIMISER": runtime.OPTIMISER, "START_ITERATIONS": runtime.START_ITERATIONS,
                 "UPDATE_ITERATIONS": runtime.UPDATE_ITERATIONS, "WIDTH": runtime.WIDTH, "HEIGHT": runtime.HEIGHT, "MODALNAME": runtime.MODALNAME}

    with open('buddy.json', 'w', encoding='utf-8') as f:
        json.dump(json_file, f, ensure_ascii=False, indent=4)


def load_configuration():

    runtime.CONFIGURATIONS = get_configuration()

    actual_config = {}

    if os.path.isfile('buddy.json'):
        with open('buddy.json', 'r', encoding='utf-8') as f:
            json_file = json.load(f)
    else:
        print('No Configuration File buddy.json, using default configuration')
        json_file = {}

    for item in runtime.CONFIGURATIONS:
        if item.name in json_file.keys():
            current_value = json_file[item.name]
            if current_value is None:
                actual_config[item.name] = item.defaultValue
            elif item.type == ConfigurationType.INT:
                current_value = int(current_value)
                if (current_value < item.minValue or current_value > item.maxValue):
                    current_value = item.defaultValue
            elif item.type == ConfigurationType.FLOAT:
                current_value = float(current_value)
                if (current_value < item.minValue or current_value > item.maxValue):
                    current_value = item.defaultValue
            actual_config[item.name] = current_value
        else:
            actual_config[item.name] = item.defaultValue

    runtime.LR = actual_config["LR"]
    runtime.OPTIMISER = actual_config["OPTIMISER"]
    runtime.START_ITERATIONS = actual_config["START_ITERATIONS"]
    runtime.UPDATE_ITERATIONS = actual_config["UPDATE_ITERATIONS"]
    runtime.WIDTH = actual_config["WIDTH"]
    runtime.HEIGHT = actual_config["HEIGHT"]
    runtime.MODALNAME = actual_config["MODALNAME"]


def get_config_value(name):
    if (name == 'LR'):
        return runtime.LR
    if (name == 'OPTIMISER'):
        return runtime.OPTIMISER
    if (name == 'START_ITERATIONS'):
        return runtime.START_ITERATIONS
    if (name == 'UPDATE_ITERATIONS'):
        return runtime.UPDATE_ITERATIONS
    if (name == 'WIDTH'):
        return runtime.WIDTH
    if (name == 'HEIGHT'):
        return runtime.HEIGHT
    if (name == 'MODALNAME'):
        return runtime.MODALNAME
    return ''


def set_config_value(name, value):
    if (name == 'LR'):
        runtime.LR = value
        return True
    if (name == 'OPTIMISER'):
        runtime.OPTIMISER = value
        return True
    if (name == 'START_ITERATIONS'):
        runtime.START_ITERATIONS = value
        return True
    if (name == 'UPDATE_ITERATIONS'):
        runtime.UPDATE_ITERATIONS = value
        return True
    if (name == 'WIDTH'):
        runtime.WIDTH = value
        return True
    if (name == 'HEIGHT'):
        runtime.HEIGHT = value
        return True
    if (name == 'MODALNAME'):
        runtime.MODALNAME = value
        return True
    return False
