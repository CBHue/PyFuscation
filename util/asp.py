import re
import os
import util.helper as helper

'''
    Available languages are C#, VB, VBSscript, JavaScript, JScript, or ECMAScript.

'''

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
                #print(i.ljust(10, ' ') + " - " + str(match.groups()).strip())

                if i in VARs:
                    continue
                else:
                        vNum = 21
                        new = helper.randomString()
                        VARs[i] = new + str(vNum)
                        ofHandle.write("Replacing: " + i + " with: " + new + "\n")
                        print("Replacing: " + i + " with: " + new + "\n")
                        vNum += 1

    # return dict of variable and their replacements
    helper.printY("Variables Replaced  : " + str(len(VARs)))
    return VARs

def findFUNCs(iFile,lFile):
    FUNCs = {}
    ofHandle = open(lFile, 'w')
    with open(iFile, "r") as f:
        for line in f:
            funcMatch = re.search(r'^\s*[a-zA-Z]+\s+([a-zA-Z0-9_-]+)\s*\(',line, re.IGNORECASE)
            if funcMatch and funcMatch.group(1) not in FUNCs: 
                if funcMatch.group(1) == "main":
                    continue
                vNum = 9999
                new = helper.randomString()
                FUNCs[funcMatch.group(1)] = new
                ofHandle.write("Replacing: " + funcMatch.group(1) + " with: " + str(new) + "\n")
                vNum += 1
    # return dict of variable and their replacements
    helper.printY("Functions Replaced  : " + str(len(FUNCs)))
    return FUNCs

def findCustomParams(iFile,oFile,VARs):
    PARAMs = {}
    READ = False
    start = 0
    end = 0
    regex = r'([\$-]\w{4,})'
    ofHandle = open(oFile, 'w')

    with open(iFile, "r") as f:
        for line in f:
            line = line.strip()

            if re.search(r'\bparam\b', line, re.I):
                # Ok we are at the begining of a custum parameter
                READ = True

                # The open paren is on another line so move until we find it
                start = start + line.count('(')
                if start == 0:
                    continue

                end   = end + line.count(')')

                v = re.findall(regex,line)
                for i in v:
                    if i.lower() not in lower_Reserverd and i not in PARAMs:
                        # Lets check to see if this has been replaced already
                        new = VARs.get(i)
                        if not new:
                            continue
                        new = " -" + new[1:]
                        old = " -" + i[1:]
                        PARAMs[old] = new
                        ofHandle.write("Replacing: " + old + " with: " + new + "\n")

                # If the params are all on one line were done here
                if start != 0 and start == end:
                    start = 0
                    end = 0
                    READ = False
                    continue
                
            # These are the custom parameters
            elif READ:
                v = re.findall(regex,line)
                for i in v:
                    if i.lower() not in lower_Reserverd and i not in PARAMs:
                        new = VARs.get(i)
                        if not new:
                            continue
                        new = " -" + new[1:]
                        old = " -" + i[1:]
                        PARAMs[old] = new
                        ofHandle.write("Replacing: " + old + " with: " + new + "\n")

                start = start + line.count('(')
                end   = end + line.count(')')
                if start != 0 and start == end:
                    start = 0
                    end = 0
                    READ = False

            # Keep moving until we have work
            else:
                continue

    helper.printY("Parameters Replaced : " + str(len(PARAMs)))
    return PARAMs