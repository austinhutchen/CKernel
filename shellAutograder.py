#!/usr/bin/env python3
from __future__ import print_function
import subprocess
import sys
import time
import re
import io
import os

testNumber = 10

##
## Be more forgiving on output comparison - remove blank spaces and put everything in lower case
##
def noBS(s):
    return s.lower().translate(str.maketrans('', '', ' \n\t\r'))

##
## This test framework had some problems for test11, test12 and test13 of the standard
## assignment. The following subprocess.Popen runs the jobs, but does not read
## all the input and some processes are left around such that when the second test
## is running, those processes would appear in the 'ps' output.
##
## I've changed the solution to read the full input and place it into a string
## buffer before running the second test. This removes this minor glitch.
##
## dirk

def runCmd(cmd): 
    proc = subprocess.Popen(cmd, bufsize=0, text=True, stdout=subprocess.PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        print("Timeout running command:", cmd)
        proc.kill()
        stdout = ""
        stderr = ""
    return stdout, stderr

def runTrace(testNumber):
    success=True
    ref_out, ref_err = runCmd(["make", "rtest%02d"%(testNumber)])
    test_out, test_err = runCmd(["make", "test%02d"%(testNumber)])

    test=io.StringIO(test_out)
    ref=io.StringIO(ref_out)

    ref_out = ref_out.splitlines() if ref_out else [""]
    ref_err = ref_err.splitlines() if ref_err else [""]
    test_out = test_out.splitlines() if test_out else [""]
    test_err = test_err.splitlines() if test_err else [""]

    testLines = [line.strip() for line in test_out ]
    refLines = [ line.strip() for line in ref_out ]
    testErr = [ line.strip() for line in test_err ]
    refErr = [ line.strip() for line in ref_err ]

    if len(testLines) != len(refLines):
        print("Your ./tsh output has a different number of lines than the reference output")
        print("Your ./tsh printed", len(testLines), "lines to stdout")
        print("The reference ./tshref printed", len(refLines), "lines to stdout")
        print("")
        print("Your ./tsh printed these lines to stdout", testLines)
        print("Your ./tsh printed these lines to stderr", testErr)
        print("")
        print("The reference ./tshref printed these lines to stdout", refLines)
        print("Your reference ./tshref printed these lines to stderr", refErr)
        return False

    testLine = test.readline().strip()
    refLine = ref.readline()

    if (testLine != './sdriver.pl -t trace%02d.txt -s ./tsh -a "-p"'%(testNumber)):
        print("\tERROR: Bad first line in test.")
        print("got *%s*"%(testLine))
        return False

    refLine = ref.readline()
    testLine = test.readline()
    while((testLine != "") or (refLine != "")):
        if refLine.strip() == "tsh> /bin/ps a":
            if noBS(testLine) != noBS(refLine):
                print("\tERROR: \"%s\" <=!=> \"%s\""%(refLine.strip(),
                                                    testLine.strip()))
                success = False
            success =  psScan(ref, test) and success
        success = normalScan(refLine, testLine) and success
        testLine = test.readline()
        refLine = ref.readline()
    return success


def normalScan(refL, testL):
    if refL == "":
        print("\tERROR: ./tshref output has fewer lines than ./tsh output.")
        return False
    elif testL == "":
        print("\tERROR: ./tsh output has fewer lines than ./tshref output.")
        return False
    elif noBS(testL) != noBS(refL):
        noPIDtest = re.sub(r'\([0-9]+\)*', '(*PID*)', testL)
        noPIDref = re.sub(r'\([0-9]+\)*', '(*PID*)', refL)
        if(noBS(noPIDtest) != noBS(noPIDref)):
            print("\t\"%s\" <=!=> \"%s\""%(noPIDtest.strip(), noPIDref.strip()))
            return False
    return True

def isProgramWeCareAbout(line):
    if "/bin/sh" in line or "/usr/bin/perl" in line:
        return False

    if "./mysplit " in line \
       or "./myspin " in line \
       or "./myint "in line \
       or "./mystop " in line \
       or "./tsh " in line:
        return True
    else:
        return False


def psScan(ref, test):
    #
    # This compares the process status(ps) of the reference solution and the test solution
    # The process status (e.g. suspended, etc) should match
    #
    success=True
    #Dict stores state, and number of lines like this we saw, for each cmd.
    refDict = {}
    testDict = {}

    #Collect ref info.
    refL = ref.readline()
    psRefHeader = refL.strip()
    refL = ref.readline()
    while(("tsh>" not in refL) and refL!=""):
        psLine = refL.strip().split(None, 4)
        if isProgramWeCareAbout(psLine[4]):
            if psLine[4] in refDict:
                refDict[psLine[4]].append(psLine[2])
            else:
                refDict[psLine[4]] = [psLine[2]]
        refL = ref.readline()
    
    #Collect test info.
    testL = test.readline()
    if(testL.strip()!=psRefHeader):
        print("\tERROR: Unexpected ps header in test.")
        success=False
    testL = test.readline()
    while(("tsh>" not in testL) and testL!=""):
        psLine = testL.strip().split(None, 4)
        if isProgramWeCareAbout(psLine[4]):
            if psLine[4] in testDict:
                testDict[psLine[4]].append(psLine[2])
            else:
                testDict[psLine[4]] = [psLine[2]]
        testL = test.readline()
    #Now, comparing the two dicts.
    for key in refDict.keys():
        try:
            if(refDict[key] != testDict[key]):
                print("\tERROR: Status for (%s) does not match:"%(key))
                print("\t\tReference Statuses: %s"%(refDict[key]))
                print("\t\tYour Statuses: %s"%(testDict[key]))
                success = False
        except KeyError:
            if "./tshref" in key:
                continue
            print("\tERROR: \"%s\" not found in test dict."%(key))
            success = False
            
    return success

def isExecutable( filename:str ):
    return os.path.isfile(filename) and os.access(filename, os.X_OK)

NeededBinaries = [ "tsh", "myspin", "mystop", "myint", "mysplit", "tshref" ]

if  not all( [ isExecutable(binary) for binary in NeededBinaries ] ):
    print("Building ./tsh and related files")
    runCmd(["make"])
    if not all( [ isExecutable(binary) for binary in NeededBinaries ] ):
        print("Unable to build tsh so can't run grader")
        sys.exit(200)

if len(sys.argv) > 1:
    for trace in sys.argv[1:]:
        i = int(trace)
        print("================================================================================")
        print("Running trace %02d..."%(i))
        if runTrace(i):
            print("\tPassed.")
        else:
            print("\tFailed.")
            sys.exit(100)
else:
    numPassed = 0
    for i in range(16):
        print("================================================================================")
        print("Running trace %02d..."%(i+1))
        if runTrace(i+1):
            numPassed+=1
            print("\tPassed.")
        else:
            print("\tFailed.")

    print("Total Passed: %d/16\tGrade: "%(numPassed),end="")
    if(numPassed>=16):
        print("100%")
        sys.exit(0)
    elif(numPassed>=13):
        print("90%")
    elif(numPassed>=10):
        print("80%")
    elif(numPassed>=8):
        print("60%")
    elif(numPassed >= 5):
        print("30%")
    elif(numPassed >= 3):
        print("10%")
    sys.exit(100)
