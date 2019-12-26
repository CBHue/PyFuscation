import os
import random

def randomString():
	wordList = os.path.abspath(os.path.dirname(__file__)) + "/wordList.txt"
	with open(wordList, "r") as f:
		line = next(f)
		for num, aline in enumerate(f, 2):
			if random.randrange(num): continue
			line = aline
		string = ''.join(e for e in line if e.isalnum())
		return string


def printR(out): print("\033[91m{}\033[00m" .format("[!] " + out)) 
def printG(out): print("\033[92m{}\033[00m" .format("[*] " + out)) 
def printY(out): print("\033[93m{}\033[00m" .format("[+] " + out)) 
def printP(out): print("\033[95m{}\033[00m" .format("[-] " + out)) 