#!/usr/bin/env python

import sys
import os

def checklogs(logfile,answerfile):
    logs = open(logfile,"r")
    answerf = open(answerfile,"r")
    answer = answerf.read().splitlines()
    steps = len(answer)
    state = 0
    for line in logs:
        if answer[state].strip() == line.split('\t')[1].strip():
            state+=1
        if state == steps:
            break
    logs.close()
    answerf.close()
    return state == steps
    
if __name__ == "__main__":
    #Check arguments
    if len(sys.argv) < 2:
        print("Error! Did not get a path where to run")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print("Error! given path does not exist")
        sys.exit(1)
    answer = os.path.join(path,"answer.txt")
    logs = os.path.join(path,"pymoult.log")
    if not (os.path.exists(answer) and os.path.exists(logs)):
        print("Error! could not find logs or results")
        sys.exit(1)
    #Now we're ready
    res = checklogs(logs,answer)
    if res:
        #We passed the test
        sys.exit(0)
    else:
        #We failed
        sys.exit(1)
