import re
import os
import util.helper as helper

def findVARs(iFile,lFile):
    VARs = {}
    vNum = 9999
    
    # ASP.NET C# : int counter = 103;
    regex = r'^\s*[a-zA-Z0-9_]+\s+([a-zA-Z0-9_]+)\s*\=\s*.*\;'

    # ASP.NET VB : Dim temp As String
    regexDIM = r'^\s*[d|D]im\s+([a-zA-Z0-9_]+)\s+'

    ofHandle = open(lFile, 'w')

    with open(iFile, "r") as f:
        for line in f:
            
            match = re.search(regexDIM + "|" + regex, line)
            if match:
                i = match.group(1)
                j = match.group(2)
                if i is None:
                    i = j
                print(i.ljust(10, ' ') + " - " + str(match.groups()).strip())

                if i in VARs:
                    continue
                else:
                        vNum = 21
                        new = helper.randomString()
                        VARs[i] = new + str(vNum)
                        ofHandle.write("Replacing: " + i + " with: " + new + "\n")
                        vNum += 1

    # return dict of variable and their replacements
    helper.printY("Variables Replaced  : " + str(len(VARs)))
    return VARs