import os
import subprocess
"""
filename is the path to the file to be compiled and execute
testcase is the path to the folder containing the testcases
number is the number of testcases
lang is the language of the source code
timeout is the timilimit in seconds
"""
filename=input()
testcase=input()
number=input()
lang=input()
timeout=input()

"""
This function compiles the source code, executes it and then runs on the testcases
The possible return values are:
    CE - Compilation Error
    AC - Accepted
    WA - Wrong Answer
    TLE - Time Limit Exceeded
    RE - Runtime Error
"""
def bashfunc(filename,testcase,number,lang,timeout):
    if lang == 'cpp': # if language is C++
        compilecommand = "g++ -std=c++11 {0} 2>compile_errors.txt".format(filename) # command to compile the source files in c++
        os.system(compilecommand)
        if os.stat("compile_errors.txt").st_size: # if any compilation errors
            os.system("rm compile_errors.txt") # returns Compilation Error
            return "CE"
        else:                                   # else running on the testcases
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            for i in range(int(number)):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "timeout {1}s ./a.out < {0} > tempout.txt 2>runtime_errors.txt".format(inpi,timeout) # Executing the compiled code with input from testcase input
                command2 = "diff tempout.txt {0} > diff.txt".format(outi) # comparing with the testcase output
                process = subprocess.Popen(command1, shell=True)
                process.communicate()
                retval=process.returncode
                if os.stat("runtime_errors.txt").st_size: # if any runtime errors
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt") # returns Runtime Error
                    return 'RE'
                if retval==124: # if the timelimit exceeds
                	os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt") # returns TimeLimit Exceeded
                	return 'TLE'
                os.system(command2)
                if os.stat("diff.txt").st_size == 0: # if the output matches with the testcase output
                    os.system("rm diff.txt") # continue with next testcase
                    correct += 1
                else:   # if the output do not match with testcase output
                    os.system("rm a.out diff.txt tempout.txt compile_errors.txt runtime_errors.txt") # returns Wrong Answer
                    return "WA"
            os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt")
            return "AC"
    elif lang == 'py3': # if is language Python3
        inputs = testcase + "input_" # running on the testcases
        outputs = testcase + "output_"
        correct = 0
        for i in range(int(number)):
            inpi = inputs + str(i+1)
            outi = outputs + str(i+1)
            command1 = "timeout {2}s python3 {0} < {1} > tempout.txt 2>runtime_errors.txt".format(filename,inpi,timeout) # Executing the code with input from testcase input
            command2 = "diff tempout.txt {0} > diff.txt".format(outi) # comparing with the testcase output
            process = subprocess.Popen(command1, shell=True)
            process.communicate()
            retval=process.returncode
            if os.stat("runtime_errors.txt").st_size:  # if any runtime errors
                os.system("rm tempout.txt runtime_errors.txt")  # returns Runtime Error
                return 'RE'
            if retval==124:  # if the timelimit exceeds
                os.system("rm tempout.txt runtime_errors.txt")  # returns TimeLimit Exceeded
                return 'TLE'
            os.system(command2)
            if os.stat("diff.txt").st_size == 0:  # if the output matches with the testcase output
                os.system("rm diff.txt")  # continue with next testcase
                correct += 1
            else:  # if the output do not match with testcase output
                os.system("rm diff.txt tempout.txt runtime_errors.txt")  # returns Wrong Answer
                return "WA"
        os.system("rm tempout.txt runtime_errors.txt")
        return "AC"
    elif lang == 'py': # if language is Python2
        inputs = testcase + "input_" # running on the testcases
        outputs = testcase + "output_"
        correct = 0
        for i in range(int(number)):
            inpi = inputs + str(i+1)
            outi = outputs + str(i+1)
            command1 = "timeout {2}s python {0} < {1} > tempout.txt 2>runtime_errors.txt".format(filename,inpi,timeout) # Executing the code with input from testcase input
            command2 = "diff tempout.txt {0} > diff.txt".format(outi) # comparing with the testcase output
            process = subprocess.Popen(command1, shell=True)
            process.communicate()
            retval=process.returncode
            if os.stat("runtime_errors.txt").st_size:  # if any runtime errors
                os.system("rm tempout.txt runtime_errors.txt")  # returns Runtime Error
                return 'RE'
            if retval==124:  # if the timelimit exceeds
                os.system("rm tempout.txt runtime_errors.txt")  # returns TimeLimit Exceeded
                return 'TLE'
            os.system(command2)
            if os.stat("diff.txt").st_size == 0:  # if the output matches with the testcase output
                os.system("rm diff.txt")  # continue with next testcase
                correct += 1
            else:  # if the output do not match with testcase output
                os.system("rm diff.txt tempout.txt runtime_errors.txt")  # returns Wrong Answer
                return "WA"
        os.system("rm tempout.txt runtime_errors.txt")
        return "AC"
        os.system("rm tempout.txt runtime_errors.txt")
        return "AC"
    elif lang == 'java':  # if language is Java
        compilecommand = "javac {0} 2>compile_errors.txt".format(filename) # command to compile the source files in Java
        os.system(compilecommand)
        if os.stat("compile_errors.txt").st_size: # if any compilation errors
            os.system("rm compile_errors.txt") # returns compilation errors
            return "CE"
        else:  # else running on the testcases
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            filei = filename[:-5]
            for i in range(int(number)):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                # Executing the compiled code with input from testcase input
                command1 = "timeout {2}s java -cp {3} {0} < {1} > tempout.txt 2>runtime_errors.txt".format(os.path.basename(filei),inpi,timeout,os.path.dirname(filename))
                command2 = "diff tempout.txt {0} > diff.txt".format(outi) # comparing with the testcase output
                os.system("echo "+command1+" > sample")
                process = subprocess.Popen(command1, shell=True)
                process.communicate()
                retval=process.returncode
                if os.stat("runtime_errors.txt").st_size: # if any runtime errors
                    os.system("rm "+filename[:-4]+"class tempout.txt compile_errors.txt runtime_errors.txt") # returns Runtime Error
                    return 'RE'
                if retval==124: # if the timelimit exceeds
                    os.system("rm "+filename[:-4]+"class tempout.txt compile_errors.txt runtime_errors.txt") # returns TimeLimit Exceeded
                    return 'TLE'
                os.system(command2)
                if os.stat("diff.txt").st_size == 0: # if the output matches with the testcase output
                    os.system("rm diff.txt") # continue with next testcase
                    correct += 1
                else:
                    os.system("rm diff.txt tempout.txt runtime_errors.txt "+filename[:-4]+"class") # if the output do not match with testcase output
                    return "WA" # returns Wrong Answer
            os.system("rm tempout.txt runtime_errors.txt "+filename[:-4]+"class")
            return "AC"
    elif lang == 'c': # if language is C
        compilecommand = "gcc {0} 2>compile_errors.txt".format(filename) # command to compile the source files in c
        os.system(compilecommand)
        if os.stat("compile_errors.txt").st_size: # if any compilation errors
            os.system("rm compile_errors.txt") # returns Compilation Error
            return "CE"
        else:                                   # else running on the testcases
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            for i in range(int(number)):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "timeout {1}s ./a.out < {0} > tempout.txt 2>runtime_errors.txt".format(inpi,timeout) # Executing the compiled code with input from testcase input
                command2 = "diff tempout.txt {0} > diff.txt".format(outi) # comparing with the testcase output
                process = subprocess.Popen(command1, shell=True)
                process.communicate()
                retval=process.returncode
                if os.stat("runtime_errors.txt").st_size: # if any runtime errors
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt") # returns Runtime Error
                    return 'RE'
                if retval==124: # if the timelimit exceeds
                	os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt") # returns TimeLimit Exceeded
                	return 'TLE'
                os.system(command2)
                if os.stat("diff.txt").st_size == 0: # if the output matches with the testcase output
                    os.system("rm diff.txt") # continue with next testcase
                    correct += 1
                else:   # if the output do not match with testcase output
                    os.system("rm a.out diff.txt tempout.txt compile_errors.txt runtime_errors.txt") # returns Wrong Answer
                    return "WA"
            os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt")
            return "AC"
    else: # if language is not one of the above languages then returns "No Language Found"
        return "no language found"
print(bashfunc(filename,testcase,number,lang,timeout))
