import os
import subprocess
def bashfunc(filename,testcase,number,lang,timeout):
    if lang == 'cpp':
        compilecommand = "g++ -std=c++14 {0} 2>compile_errors.txt".format(filename)
        os.system(compilecommand)
        if os.stat("compile_errors.txt").st_size:
            os.system("rm compile_errors.txt")
            return "CE"
        else:
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            for i in range(number):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "./test.sh './a.out' < {0} > tempout.txt 2>runtime_errors.txt & PID=$!; sleep {1}; kill $PID 2>time_errors.txt".format(inpi,timeout)
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                os.system(command1)
                if os.stat("runtime_errors.txt").st_size:
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt time_errors.txt")
                    return 'RE'
                if os.stat("time_errors.txt").st_size == 0:
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt time_errors.txt")
                    return 'TLE'
                os.system(command2)
                if os.stat("diff.txt").st_size == 0:
                    os.system("rm diff.txt")
                    correct += 1
                else:
                    os.system("rm a.out diff.txt tempout.txt compile_errors.txt runtime_errors.txt time_errors.txt")
                    return "WA"
            os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt time_errors.txt")
            return "AC"
    elif lang == 'py3':
        inputs = testcase + "input_"
        outputs = testcase + "output_"
        correct = 0
        for i in range(number):
            inpi = inputs + str(i+1)
            outi = outputs + str(i+1)
            command1 = "./test.sh 'python3 {0}' < {1} > tempout.txt 2>runtime_errors.txt & PID=$!; sleep {2}; kill $PID 2>time_errors.txt".format(filename,inpi,timeout)
            command2 = "diff tempout.txt {0} > diff.txt".format(outi)
            os.system(command1)
            if os.stat("runtime_errors.txt").st_size:
                os.system("rm tempout.txt runtime_errors.txt time_errors.txt")
                return 'RE'
            if os.stat("time_errors.txt").st_size == 0:
                os.system("rm tempout.txt runtime_errors.txt time_errors.txt")
                return 'TLE'
            os.system(command2)
            if os.stat("diff.txt").st_size == 0:
                os.system("rm diff.txt")
                correct += 1
            else:
                os.system("rm diff.txt tempout.txt runtime_errors.txt time_errors.txt")
                return "WA"
        os.system("rm tempout.txt runtime_errors.txt time_errors.txt")
        return "AC"
    elif lang == 'py':
        inputs = testcase + "input_"
        outputs = testcase + "output_"
        correct = 0
        for i in range(number):
            inpi = inputs + str(i+1)
            outi = outputs + str(i+1)
            command1 = "./test.sh 'python {0}' < {1} > tempout.txt 2>runtime_errors.txt & PID=$!; sleep {2}; kill $PID 2>time_errors.txt".format(filename,inpi,timeout)
            command2 = "diff tempout.txt {0} > diff.txt".format(outi)
            os.system(command1)
            if os.stat("runtime_errors.txt").st_size:
                os.system("rm tempout.txt runtime_errors.txt time_errors.txt")
                return 'RE'
            if os.stat("time_errors.txt").st_size == 0:
                os.system("rm tempout.txt runtime_errors.txt time_errors.txt")
                return 'TLE'
            os.system(command2)
            if os.stat("diff.txt").st_size == 0:
                os.system("rm diff.txt")
                correct += 1
            else:
                os.system("rm diff.txt tempout.txt runtime_errors.txt time_errors.txt")
                return "WA"
        os.system("rm tempout.txt runtime_errors.txt time_errors.txt")
        return "AC"
    elif lang == 'java':
        compilecommand = "javac {0} 2>compile_errors.txt".format(filename)
        os.system(compilecommand)
        if os.stat("compile_errors.txt").st_size:
            os.system("rm compile_errors.txt")
            return "CE"
        else:
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            filei = filename[:-5]
            for i in range(number):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "./test.sh 'java {0}' < {1} > tempout.txt 2>runtime_errors.txt & PID=$!; sleep {2}; kill $PID 2>time_errors.txt".format(filei,inpi,timeout)
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                os.system(command1)
                if os.stat("runtime_errors.txt").st_size:
                    os.system("rm *.class tempout.txt runtime_errors.txt time_errors.txt")
                    return 'RE'
                if os.stat("time_errors.txt").st_size == 0:
                    os.system("rm *.class tempout.txt runtime_errors.txt time_errors.txt")
                    return 'TLE'
                os.system(command2)
                if os.stat("diff.txt").st_size == 0:
                    os.system("rm diff.txt")
                    correct += 1
                else:
                    os.system("rm diff.txt tempout.txt runtime_errors.txt time_errors.txt *.class")
                    return "WA"
            os.system("rm tempout.txt runtime_errors.txt time_errors.txt *.class")
            return "AC"
    elif lang == 'c':
        compilecommand = "gcc {0} 2>compile_errors.txt".format(filename)
        os.system(compilecommand)
        if os.stat("compile_errors.txt").st_size:
            os.system("rm compile_errors.txt")
            return "CE"
        else:
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            for i in range(number):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "./test.sh './a.out' < {0} > tempout.txt 2>runtime_errors.txt & PID=$!; sleep {1}; kill $PID 2>time_errors.txt".format(inpi,timeout)
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                os.system(command1)
                if os.stat("runtime_errors.txt").st_size:
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt time_errors.txt")
                    return 'RE'
                if os.stat("time_errors.txt").st_size == 0:
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt time_errors.txt")
                    return 'TLE'
                os.system(command2)
                if os.stat("diff.txt").st_size == 0:
                    os.system("rm diff.txt")
                    correct += 1
                else:
                    os.system("rm a.out diff.txt tempout.txt compile_errors.txt runtime_errors.txt time_errors.txt")
                    return "WA"
            os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt time_errors.txt")
            return "AC"
    else:
        return "no language found"
