import os
import re
import random
import shlex
import subprocess
import fileinput

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
    # Remove // Comments
    cmd = "sed -i \'/\/\/.*$/d\' " + oF
    realTimeMuxER(cmd)
    # Remove empty Space
    cmd = "sed -i -e \'s/^[[:space:]]*#.*$//g\' " + oF
    realTimeMuxER(cmd)
    # Delete blank lines
    cmd = "sed -i \'/^$/d\' " + oF
    realTimeMuxER(cmd)
    # Remove HTML comments 
    cmd = "sed -i -e :a -re '/<!--.*?-->/d;/<!--/N;//ba' "  + oF
    realTimeMuxER(cmd)

def useSED(DICT, oF):
	for old in DICT:
		new = str(DICT.get(old))
		#cmd = "sed -i -e \'s/" + old + '\\>' + "/" + new + "/g\' " + oF
		#cmd = "sed -i -e \'s/" + '[\\>|\\<|\\b|[:space:]]' + old + '[\\>|\\<|\\b|[:space:]]' + "/ " + new + " /g\' " + oF
		#cmd = "sed -i -e \'s/" + '[\\>|\\<|\\b|[:space:]]' + old + '\\>' + "/" + new + "/g\' " + oF
		#cmd = "sed -i -e \'s/" + '\\W' + old + '\\>' + "/" + new + "/g\' " + oF
		#cmd = "sed -i -e \'s/" + '[^a-zA-Z0-9]' + old + '[^a-zA-Z0-9]' + "/" + new + "/g\' " + oF
		cmd = "sed -i -e \'s/" + old + '\\b' + "/" + new + "/g\' " + oF
		#print(cmd)
		realTimeMuxER(cmd)

def THEreplacER(DICT, oF):
	#iFHandle = open(iF, 'r')
	#ofHandle = open(oF, 'w')

	# Loop over each word to be replaced
	for old in DICT:
		new = str(DICT.get(old))

		# This means that r'\bfoo\b' matches 'foo', 'foo.', '(foo)', 'bar foo baz' but not 'foobar' or 'foo3'.
		regex = r'%s\b' % re.escape(old)
		# Trying to match $Computer but not $happy$computer
		with fileinput.input(files=oF,inplace=True) as f:
			for line in f:
				if re.search(regex, line):
					# This is kinda hacky ... 
					sLine = line.split(" ")
					nLine = ""
					for word in sLine:
						if re.search(regex, word):
							word = word.strip()
							w = word.replace(old, new)
							nLine = nLine + " " + w
						else:
							nLine = nLine + " " + word

					line = nLine
					print(line.strip())
				else:
					print(line.strip())
