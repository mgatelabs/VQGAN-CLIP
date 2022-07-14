#!/usr/bin/python

from pathlib import Path
import sys
import random
import shutil
import subprocess

from shortcuts import enhance_image
from shortcuts import make_video
from shortcuts import gen_image

#!/bin/bash
# Example "Zoom" movie generation
# e.g. python ./zoom.py "A painting of zooming in to a surreal, alien world" Zoom.png 180
# -ckpt checkpoints/wikiart_16384.ckpt -conf checkpoints/wikiart_16384.yaml

TEXT=sys.argv[1]
FILENAME=sys.argv[2]
MAX_EPOCHS=int(sys.argv[3])
RESIZE = True
VIDEO = False

#MODELNAME = 'vqgan_imagenet_f16_16384'
#MODELNAME = 'wikiart_16384'
MODELNAME = 'coco'

LR = 0.1
OPTIMISER = "Adam"
MAX_ITERATIONS = 25
MAX_ITERATIONS = 700
MAX_ITERATIONS = 400
SEED = random.randint(13, 99999999) # Keep the same seed each epoch for more deterministic runs
SCALE_FACTOR = 1.01 # Default
SCALE_FACTOR = 1.025 # Faster

# Extract
FILENAME_NO_EXT = Path(FILENAME).stem #${FILENAME%.*}
FILE_EXTENSION = Path(FILENAME).suffix

print('Frame 0')
gen_image(TEXT, OPTIMISER, SEED, MAX_ITERATIONS, MODELNAME, FILENAME, LR, None)
shutil.copyfile(FILENAME, FILENAME_NO_EXT+"-0000" + FILE_EXTENSION) #cp "$FILENAME" "$FILENAME_NO_EXT"-0000."$FILE_EXTENSION"
cmds = ['magick', FILENAME, '-distort', 'SRT', f'{SCALE_FACTOR},0', '-gravity', 'center', FILENAME]
subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8') #convert "$FILENAME" -distort SRT 1.01,0 -gravity center "$FILENAME"	# Zoom
if RESIZE:
    enhance_image(FILENAME_NO_EXT + "-0000" + FILE_EXTENSION)
    #cmds = ['realesrgan-ncnn-vulkan.exe', '-i', FILENAME_NO_EXT + "-0000" + FILE_EXTENSION, '-o', FILENAME_NO_EXT + "-0000" + FILE_EXTENSION, '-n', 'realesrgan-x4plus']
    #subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8')

if VIDEO:
    # Feedback image loop
    for i in range(1, MAX_EPOCHS):
        print(f'Frame {i}')
        padded_count = str(i).zfill(4) # padded_count=$(printf "%04d" "$i")
        gen_image(TEXT, OPTIMISER, SEED, MAX_ITERATIONS, MODELNAME, FILENAME, LR, FILENAME)
        shutil.copyfile(FILENAME, FILENAME_NO_EXT + "-" + padded_count + FILE_EXTENSION) #  cp "$FILENAME" "$FILENAME_NO_EXT"-"$padded_count"."$FILE_EXTENSION"    
        cmds = ['magick', FILENAME, '-distort', 'SRT', f'{SCALE_FACTOR},0', '-gravity', 'center', FILENAME]
        subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8') #  convert "$FILENAME" -distort SRT 1.01,0 -gravity center "$FILENAME" # Zoom
        if RESIZE:
            enhance_image(FILENAME_NO_EXT + "-" + padded_count + FILE_EXTENSION)
            #cmds = ['realesrgan-ncnn-vulkan.exe', '-i', FILENAME_NO_EXT + "-" + padded_count + FILE_EXTENSION, '-o', FILENAME_NO_EXT + "-" + padded_count + FILE_EXTENSION, '-n', 'realesrgan-x4plus']
            #subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8')
    # Make video - Nvidia GPU expected
    make_video(FILENAME_NO_EXT + '-%04d' + FILE_EXTENSION)