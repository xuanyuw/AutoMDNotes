import yaml
import re
from os.path import join, exists
from os import makedirs, listdir
from shutil import copy

with open('config.yml', 'r') as c:
    configs =  yaml.load(c, Loader=yaml.Loader)

# add image files in assets folder
dest_dir = join(configs['Obsidian_asset_dir'], configs['NoteTitle'])
if not exists(dest_dir):
    makedirs(dest_dir)

for i in range(configs['Iter']):
    for f in configs['FilesToInclude']:
        fname = f.replace('%d', str(i))
        src_path = join(configs['Image_dir'], fname)
        copy(src_path, dest_dir)  
 
for folder in configs['FoldersToInclude']:
    if '%d' in folder:
        for i in range(configs['Iter']):
            fdname = folder.replace('%d', str(i))
            src_path = join(configs['Image_dir'], fdname)
            dest_path = join(dest_dir, fdname)
            if not exists(dest_path):
                makedirs(dest_path)
            for f in listdir(src_path):
                copy(join(src_path, f), dest_path)   
    else:
        src_path = join(configs['Image_dir'], folder)
        dest_path = join(dest_dir, folder)
        if not exists(dest_path):
            makedirs(dest_path)
        for f in listdir(src_path):
            copy(join(src_path, f), dest_path)    

# Parse template and replace corresponding elements
temp = open('template.md', 'r')
l = temp.readline()
newText = ''
while l:
    if l.count('=') == 2:
        if 'TITLE' in l:
            newStr = re.sub('=(.*)=', configs['NoteTitle'], l)
            newText = newText+newStr
        elif l=='=LOOP=':
            l = temp.readline()
            for i in range(configs['Iter']):


    else:
        newText = newText + l
    
    newText = newText + '\n'
    l = temp.readline()
              
def createLoopedLines(temp, configs):
    ll = ''

    return ll

def getLoopPattern(temp):
    lp = ''
    l = temp.readline()
    while l != '=ENDLOOP=':
        lp = lp + l + '\n'
    return lp