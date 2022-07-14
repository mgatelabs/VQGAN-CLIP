import subprocess

def enhance_image(image_path):
    cmds = ['realesrgan-ncnn-vulkan.exe', '-i', image_path, '-o', image_path, '-n', 'realesrgan-x4plus']
    subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8')

def make_video(file_pattern):
    cmds = ['ffmpeg', '-y', '-i', file_pattern, '-b:v', '8M', '-c:v', "h264_nvenc", '-pix_fmt', 'yuv420p', '-strict', '-2', '-filter:v', "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60'", 'video.mp4']
    #ffmpeg -y -i "$FILENAME_NO_EXT"-%04d."$FILE_EXTENSION" -b:v 8M -c:v h264_nvenc -pix_fmt yuv420p -strict -2 -filter:v "minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60'" video.mp4
    subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8')

def gen_image(PROMPT, OPTIMISER, SEED, ITTERATIONS, MODELNAME, OUTPUT_FILENAME, LR, INPUT_IMAGE):
    cmds = []
    # Program
    cmds.append('python')
    cmds.append('generate.py')
    # Size
    cmds.append('-s')
    cmds.append('390')
    cmds.append('390')
    # Prompt
    cmds.append('-p')
    cmds.append(PROMPT)
    cmds.append('-opt')
    cmds.append(OPTIMISER)    
    cmds.append('--seed')
    cmds.append(str(SEED))    
    #-i Number of iterations
    cmds.append('-i')
    cmds.append(str(ITTERATIONS))
    # -se Save image iterations
    cmds.append('-se')
    cmds.append('100')  
    # Checkpoint
    cmds.append('-ckpt')
    cmds.append(f'checkpoints/{MODELNAME}.ckpt')
    cmds.append('-conf')
    cmds.append(f'checkpoints/{MODELNAME}.yaml')
    cmds.append('-o')
    cmds.append(OUTPUT_FILENAME)
    cmds.append('-lr')
    cmds.append(str(LR))
    if INPUT_IMAGE is not None:
        cmds.append('-ii')
        cmds.append(INPUT_IMAGE)
    # Run it
    subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8')

def make_image(filename, width, height):
    cmds = []
    cmds.append('magick')
    cmds.append('-size')
    cmds.append(str(width) + 'x' + str(height))
    cmds.append('-depth')
    cmds.append('32')
    cmds.append("xc:orange")
    cmds.append(filename)
    subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8')
    
def insert_image(target_filename, insert_image, offset_x, offset_y):
    cmds = []
    cmds.append('magick')
    cmds.append(target_filename)
    cmds.append(insert_image)
    cmds.append('-depth')
    cmds.append('32')
    cmds.append('-gravity')
    cmds.append('northwest')
    cmds.append('-geometry')
    cmds.append('+' + str(offset_x) +'+' + str(offset_y))
    cmds.append('-composite')
    cmds.append(target_filename)
    subprocess.run(cmds, stdout=subprocess.PIPE).stdout.decode('utf-8')