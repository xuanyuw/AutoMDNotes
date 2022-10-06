import re
from os.path import join

def createLoopedLines(lp, configs, all_dest_path):
    ll = ''
    lp_lines = lp.splitlines()
    for i in range(configs['Iter']):
        for l in lp_lines:
            if l.count('=') == 2:
                if 'ITER' in l:
                    newStr = re.sub('=(.*)=', str(i), l)
                    ll += newStr
                else:
                    k = re.search('=(.*)?=', l)[1]
                    if k in configs['customTags'].keys():
                        s =  '![['+re.escape(join(all_dest_path[i], configs['customTags'][k]))+']]'
                        s = s.replace('\.', '.')
                        s = s.replace('\\\\', '/')
                        newStr = re.sub('=(.*)=',s, l)
                        newStr = re.sub('%d', str(i), newStr)
                        ll += newStr
            else:
                ll += l
            if '\n' not in l:
                ll += '\n'
    return ll


def getLoopPattern(temp):
    lp = ''
    l = temp.readline()
    while '=ENDLOOP=' not in l:
        lp += l
        if '\n' not in l:
            lp += '\n'
        l = temp.readline()
    return lp