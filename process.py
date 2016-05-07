from os import walk, rename, listdir, path
from subprocess import call
from argparse import ArgumentParser, FileType

def safe_rename(src, dst):
    i = 1
    if path.exists(dst):
        new_dst = dst + "_" + str(i).zfill(3)
        while path.exists(new_dst):
            i += 1
            new_dst = dst + "_" + str(i).zfill(3)
        rename(src, new_dst)
    else:
        rename(src, dst)


parser = ArgumentParser(description='process recorded mandarin sounds.')

parser.add_argument('-i', '--input-file', type=FileType('r'))
parser.add_argument('-n', '--name', type=str)

input_file = parser.parse_args().input_file
name = parser.parse_args().name

lst = input_file.read().splitlines()
names = []
for i in lst:
    if len(i) > 0:
        names.append(i.split(' ')[1])

call("sox recording_" + name + ".mp3 " + name + ".mp3 "
        "silence 1 .25 0.1% 1 0.1 0.1% : newfile : restart",shell=True)


filenames = [files for files in listdir() if (files.endswith('.mp3') &
    files.startswith(name))]
filenames.sort()
call("rm " + filenames[-1],shell=True)

for i in range(len(names)):
    rename(filenames[i],names[i]+"__" + name +".mp3")


