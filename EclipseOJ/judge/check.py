import os
import subprocess
def bashfunc(filename,testcase,number,lang,timeout):
    if lang == 0:
        bashCommand = "g++ -std=c++14 {0}".format(filename)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if process.communicate()[1]:
            return "CE"
        else:
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            for i in range(number):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "./a.out < {0} > tempout.txt & PID=$!; sleep {1}; kill $PID".format(inpi,timeout)
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                command3 = "rm a.out diff.txt tempout.txt"
                result1 = subprocess.call(command1, shell = True)
                if not result1:
                    os.system(command3)
                    return "TLE"
                os.system(command2)
                if os.stat("diff.txt").st_size == 0:
                    correct += 1
                else:
                    os.system(command3)
                    return "WA"
            os.system(command3)
            return "AC"
    elif lang == 1:
        inputs = testcase + "input_"
        outputs = testcase + "output_"
        correct = 0
        for i in range(number):
            inpi = inputs + str(i+1)
            outi = outputs + str(i+1)
            command1 = "python3 {0} < {1} > tempout.txt & PID=$!; sleep {2}; kill $PID".format(filename,inpi,timeout)
            command2 = "diff tempout.txt {0} > diff.txt".format(outi)
            command3 = "rm tempout.txt diff.txt"
            result1 = subprocess.call(command1, shell = True)
            if not result1:
                os.system(command3)
                return "TLE"
            os.system(command2)
            if os.stat("diff.txt").st_size == 0:
                correct += 1
            else:
                os.system(command3)
                return "WA"
        os.system(command3)
        return "AC"
    elif lang == 2:
        inputs = testcase + "input_"
        outputs = testcase + "output_"
        correct = 0
        for i in range(number):
            inpi = inputs + str(i+1)
            outi = outputs + str(i+1)
            command1 = "python {0} < {1} > tempout.txt & PID=$!; sleep {2}; kill $PID".format(filename,inpi,timeout)
            command2 = "diff tempout.txt {0} > diff.txt".format(outi)
            command3 = "rm tempout.txt diff.txt"
            result1 = subprocess.call(command1, shell = True)
            if not result1:
                os.system(command3)
                return "TLE"
            os.system(command2)
            if os.stat("diff.txt").st_size == 0:
                correct += 1
            else:
                os.system(command3)
                return "WA"
        os.system(command3)
        return "AC"
    elif lang == 3:
        bashCommand = "javac {0}".format(filename)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if process.communicate()[1]:
            return "CE"
        else:
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            filei = filename[:-5]
            for i in range(number):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "java {0} < {1} > tempout.txt & PID=$!; sleep {2}; kill $PID".format(filei,inpi,timeout)
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                command3 = "rm *.class tempout.txt diff.txt"
                result1 = subprocess.call(command1, shell = True)
                if not result1:
                    os.system(command3)
                    return "TLE"
                os.system(command2)
                if os.stat("diff.txt").st_size == 0:
                    correct += 1
                else:
                    os.system(command3)
                    return "WA"
            os.system(command3)
            return "AC"
    elif lang == 4:
        bashCommand = "gcc {0}".format(filename)
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if process.communicate()[1]:
            return "CE"
        else:
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            for i in range(number):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "./a.out < {0} > tempout.txt & PID=$!; sleep {1}; kill $PID".format(inpi,timeout)
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                command3 = "rm a.out diff.txt tempout.txt"
                result1 = subprocess.call(command1, shell = True)
                if not result1:
                    os.system(command3)
                    return "TLE"
                os.system(command2)
                if os.stat("diff.txt").st_size == 0:
                    correct += 1
                else:
                    os.system(command3)
                    return "WA"
            os.system(command3)
            return "AC"
    else:
        return "no language found"
