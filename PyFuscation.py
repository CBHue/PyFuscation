#!/usr/bin/env python3

'''
 
 	PyFuscation.py
    This python3 script obfuscates powershell function, variable and parameters in an attempt to bypass AV blacklists 

'''

import os
import sys
import time
import shutil
from argparse import ArgumentParser

import banner
import util.asp as asp
import util.power as power
import util.helper as helper

def main():
    iFile = args.script
    sType = "CBH"

    helper.printY("Obfuscating : " + "\033[94m" + iFile)

    if (".ps1" in args.script):
        helper.printY("File Type   : " + "\033[94m" + "Powershell")
        sType = "power"
    elif (".asp" in args.script):
        helper.printY("File Type   : " + "\033[94m" + "ASP")
        sType = "asp"
    elif (".jsp" in args.script):
        helper.printY("File Type   : " + "\033[94m" + "JSP")
        sType = "asp"
    else:
        helper.printR("Unknown File Type: " + args.script)
        exit()

    fileName, exTension = os.path.splitext(iFile)
    ts = time.strftime("%m%d%Y_%H_%M_%S", time.gmtime())
    oDir = os.path.dirname(args.script) + "/" + ts
    os.mkdir( oDir );

    oFile = oDir + "/" + ts + exTension
    vFile = oDir + "/" + ts + ".variables"
    fFile = oDir + "/" + ts + ".functions"
    pFile = oDir + "/" + ts + ".parameters"

    shutil.copy(args.script, oFile)
    helper.printY("Out File    : " + "\033[94m" + oFile)    

    obfuVAR     = dict()
    obfuPARMS   = dict()
    obfuFUNCs   = dict()

    # Remove White space and comments
    if (args.white or args.all):
        helper.printY("Comments Replaced   : *")
        helper.removeJunk(oFile)

    # Obfuscate Variables
    if (args.var or args.all):
        obfuVAR = globals()[sType].findVARs(iFile,vFile) 
        #helper.useSED(obfuVAR, oFile)
        helper.THEreplacER(obfuVAR, oFile)
        helper.printP("Obfuscated Variables located  : " + vFile)

    # Obfuscate custom parameters
    if (args.par or args.all):
        obfuPARMS = globals()[sType].findCustomParams(iFile, pFile, obfuVAR)
        helper.useSED(obfuPARMS, oFile)
        #helper.THEreplacER(obfuPARMS, oFile)
        helper.printP("Obfuscated Parameters located : " + pFile)

    # Obfuscate Functions
    if (args.func or args.all):
        obfuFUNCs = globals()[sType].findFUNCs(iFile, fFile)
        helper.useSED(obfuFUNCs, oFile)
        #helper.THEreplacER(obfuFUNCs, oFile)

        # Print the Functions
        print("")
        print("Obfuscated Function Names")
        print("-------------------------")     
        sorted_list=sorted(obfuFUNCs)
        for i in sorted_list:
            helper.printG("Replaced " + i + " With: " + obfuFUNCs[i])
        print("")    
        helper.printP("Obfuscated Functions located  : " + fFile)

    helper.printP("Obfuscated script located at  : " + oFile)

if __name__ == "__main__":
    
    if sys.version_info <= (3, 0):
        sys.stdout.write("This script requires Python 3.x\n")
        sys.exit(1)

    banner.banner()
    banner.title()

    parser = ArgumentParser()
    parser.add_argument("-f",    dest="func",    help="Obfuscate functions",        action="store_true")
    parser.add_argument("-v",    dest="var",     help="Obfuscate variables",        action="store_true")
    parser.add_argument("-p",    dest="par",     help="Obfuscate parameters",       action="store_true")
    parser.add_argument("-w",    dest="white",   help="Remove WhiteSpace/Comments", action="store_true")
    parser.add_argument("--all", dest="all",     help="Obfuscate All",              action="store_true")    
    parser.add_argument("--ps",  dest="script",  help="Obfuscate Script")
    args = parser.parse_args()

    # Powershell script
    if (args.script is None):
        parser.print_help()
        exit()
    else:
        # Check if the input file is valid:
        if not os.path.isfile(args.script):
            helper.printR("Check File: " + args.script)
            exit()  
    main()
