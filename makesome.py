#!/usr/bin/python

from pathlib import Path
import sys
import random
import shutil
import subprocess
import math

from shortcuts import gen_image
from shortcuts import make_image
from shortcuts import insert_image

# e.g. python ./makesome.py "A painting of zooming in to a surreal, alien world" Zoom 15

TEXT=sys.argv[1]
PREFIX=sys.argv[2]
MAX_EPOCHS=int(sys.argv[3])

IMAGE_SIZE = 400
IMAGE_OFFSET = 5

#MODELNAME = 'vqgan_imagenet_f16_16384'
#MODELNAME = 'wikiart_16384'
MODELNAME = 'coco'

LR = 0.1
OPTIMISER = "Adam"
MAX_ITERATIONS = 750

for i in range(0, MAX_EPOCHS):
    SEED = random.randint(13, 99999999)
    print(f'Frame: {i} - Seed: {SEED}')
    gen_image(TEXT, OPTIMISER, SEED, MAX_ITERATIONS, MODELNAME, PREFIX + str(i) + ".png", LR, None)

columns = 3;
rows = math.floor(MAX_EPOCHS / 3)
if MAX_EPOCHS % 3 != 0:
    rows += 1

target_file = PREFIX + '.png'

make_image(target_file, IMAGE_SIZE * columns, IMAGE_SIZE * rows)

for i in range(0, MAX_EPOCHS):
    column = i % 3;
    row = math.floor(i / 3)
    insert_image(target_file, PREFIX + str(i) + ".png", (IMAGE_OFFSET + (column * IMAGE_SIZE)), (IMAGE_OFFSET + (row * IMAGE_SIZE)))