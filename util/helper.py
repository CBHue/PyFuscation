import os
import random
import shlex
import subprocess

def randomString():
	wordList = os.path.abspath(os.path.dirname(__file__)) + "/wordList.txt"
	with open(wordList, "r") as f:
		line = next(f)
		for num, aline in enumerate(f, 2):
			if random.randrange(num): continue
			line = aline
		string = ''.join(e for e in line if e.isalnum())
		return string

def realTimeMuxER(command):
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = p.stdout.readline().decode()
        if output == '' and p.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = p.poll()

def printR(out): print("\033[91m{}\033[00m" .format("[!] " + out)) 
def printG(out): print("\033[92m{}\033[00m" .format("[*] " + out)) 
def printY(out): print("\033[93m{}\033[00m" .format("[+] " + out)) 
def printP(out): print("\033[95m{}\033[00m" .format("[-] " + out)) 

def removeJunk(oF):
    # general cleanup 
    cmd = "sed -i -e \'/<#/,/#>/c\\\\\' " + oF
    realTimeMuxER(cmd)
    cmd = "sed -i -e \'s/^[[:space:]]*#.*$//g\' " + oF
    realTimeMuxER(cmd)
    # Delete blank lines
    cmd = "sed -i \'/^$/d\' " + oF
    realTimeMuxER(cmd)
    # Remove HTML comments 
    cmd = "sed -i -e :a -re '/<!--.*?-->/d;/<!--/N;//ba' "  + oF
    realTimeMuxER(cmd)

def useSED(DICT, oF):
    for var in DICT:
        new = str(DICT.get(var))
        cmd = "sed -i -e \'s/" + '\\<' + var + '\\>' + "/" + new + "/g\' " + oF
        realTimeMuxER(cmd)
