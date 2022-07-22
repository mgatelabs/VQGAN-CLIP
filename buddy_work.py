#!/usr/bin/python

from glob import glob
import os
import buddy_utilities
import shortcuts
import buddy_packages
import buddy_globals as gl


def queue_enhance(package_data, file_index):
    gl.runtime.WORK_QUEUE.append(
        {"package_id": package_data['id'], 'file_index': file_index, "mode": "enhance"})


def enhance_package_file(package_data, file_index):
    filepath = buddy_utilities.get_package_image_path(
        package_data['id'], file_index)
    if os.path.isfile(filepath):
        print('Updating Image ' + filepath)
        shortcuts.gen_image(package_data['text'], gl.runtime.OPTIMISER, package_data['files']
                            [file_index]['seed'], gl.runtime.UPDATE_ITERATIONS, gl.runtime.MODALNAME, filepath, gl.runtime.LR, filepath)
    else:
        print('Generating Image ' + filepath)
        shortcuts.gen_image(package_data['text'], gl.runtime.OPTIMISER, package_data['files']
                            [file_index]['seed'], gl.runtime.START_ITERATIONS, gl.runtime.MODALNAME, filepath, gl.runtime.LR, None)


def execute_queue():
    for item in gl.runtime.WORK_QUEUE:
        if item['mode'] == 'enhance':
            package_data = buddy_packages.load_package(item["package_id"])
            file_index = item['file_index']
            enhance_package_file(package_data, file_index)
        elif item['mode'] == 'preview':
            pass
    gl.runtime.WORK_QUEUE.clear()
