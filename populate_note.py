from distutils.command.config import config
import yaml
import re
from os.path import join, exists
from os import makedirs, listdir
from shutil import copy
from  utils import getLoopPattern, createLoopedLines

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
        fdname = configs['FoldersToInclude'][1].replace('%d', str(i))
        dest_path = join(configs['Obsidian_asset_dir'], configs['NoteTitle'], fdname)
        if not exists(dest_path):
            makedirs(dest_path)
        copy(src_path, dest_path)  
 
all_dest_path = [];
for folder in configs['FoldersToInclude']:
    if '%d' in folder:
        for i in range(configs['Iter']):
            fdname = folder.replace('%d', str(i))
            src_path = join(configs['Image_dir'], fdname)
            dest_path = join(dest_dir, fdname)
            all_dest_path.append(join(configs['Asset_rel_dir'], configs['NoteTitle'], fdname))
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
            newText += newStr
        elif '=LOOP=' in l:
            lp = getLoopPattern(temp)
            ll = createLoopedLines(lp, configs, all_dest_path)
            newText += ll 
            while '=ENDLOOP=' not in l and not l:
                l = temp.readline()
        else:
            k = re.search('=(.*)?=', l)[1]
            if k in configs['customTags'].keys():
                newStr = re.sub('=(.*)=', '![['+join(configs['Asset_rel_dir'], configs['NoteTitle'], configs['FoldersToInclude'][0],configs['customTags'][k])+']]', l)
                newText += newStr
    else:
        newText += l   
    if '\n' not in l:
        newText = newText + '\n'
    l = temp.readline()

with open(join(configs['Obsidian_dir'],'testFile.md'), 'w') as f:
    f.write(newText)