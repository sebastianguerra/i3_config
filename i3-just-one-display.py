#!/usr/bin/env python

from json import loads
from os import popen 
from sys import argv

def ipc_query(req="command", msg=""):
    ans = popen("i3-msg -t " + req + " " + msg).readlines()[0]
    return loads(ans)

if __name__ == "__main__":
    # Usage & checking args
    if len(argv) != 2:
        print("Usage: /path/to/i3-just-one-display.py name-of-workspace")
        exit(-1)

    newWorkspace = argv[1]
    prevWorkspace = None
 
    # Retrieving active display
    activeDisplay = None
    secondDisplay = None
    workspacesList = ipc_query(req="get_workspaces") 
    for w in workspacesList:
        if w['focused']:
            activeDisplay = w['output']
            prevWorkspace = w['name']
        if w['name'] == newWorkspace:
            secondDisplay = w['output']
    if secondDisplay == None or activeDisplay == secondDisplay:
        print(ipc_query(msg="'workspace "+newWorkspace+"'"))
        exit(0)
    
    command = "'";
    for w in workspacesList:
        if w['output'] == activeDisplay:
            command+="workspace "+w['name']+"; move workspace to output "+secondDisplay+";"
        elif w['output'] == secondDisplay:
            command+="workspace "+w['name']+"; move workspace to output "+activeDisplay+";"
    command+="workspace "+prevWorkspace+"; workspace "+newWorkspace+";'" 
    ipc_query(msg=command)
    
    exit(0)
