#!/home/python/bin/python
#-*- coding:utf-8 -*-

from subprocess import PIPE, Popen
import re
import sys

def getMemInfo():
    p = Popen(['dmidecode'], shell = False, stdout = PIPE)
    stdout, stderr = p.communicate()
    return stdout.strip()

def parserMemInfo(memdata):
    line_in = False
    mem_str = ''
    pd = {}
    fd = {}
    for line in memdata.split('\n'):    # read each line
        if line.startswith('Memory Device') and line.endswith('Memory Device'): # if single line's content is 'Memory Device' exactly
            line_in = True
            mem_str += '\n'     # create a new line if match content
            continue            # go next for loop, don't exec following script
        if line.startswith('\t') and line_in:
            mem_str += line     # write the content what we need
            #print mem_str
        else:                   # blank line or other content
            line_in = False
    #print mem_str

    for i in mem_str.split('\n')[1:]:   # Using slice because there is '\n' at top line, we need delete it first!
        #print i
        lines = i.replace('\t', '\n').strip()   # print multiple lines instead of '1 item 1 line only'
        #print lines
        for ln in lines.split('\n'):
            k, v = [i for i in ln.split(':')]   # read key:value in single line
            pd[k.strip()] = v.strip()
        #print pd       # output JSON format dict now, contains all infos
        if pd['Size'] != 'No Module Installed': # if memory be installed at this slot
            mem_info = 'Size: %s; Part_Number: %s; Manufacturer: %s; Locator: %s; Serial_Number: %s' % (pd['Size'], pd['Part Number'], pd['Manufacturer'], pd['Locator'], pd['Serial Number'])
            #print mem_info     # output JSON format dict, which only print installed memory
            for line in mem_info.split('\n'):
                for word in line.split(';'):
                    k, v = [j.strip() for j in word.split(':')] # read key:value again, this time, we read what we need exactly
                    fd[k.strip()] = v.strip()
                yield fd

if __name__ == '__main__':
    memdata = getMemInfo()
    parserMemInfo(memdata)
    for i in parserMemInfo(memdata):
        print i
