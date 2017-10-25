import os
import subprocess
filename=input()
testcase=input()
number=input()
lang=input()
timeout=input()
def bashfunc(filename,testcase,number,lang,timeout):
    if lang == 'cpp':
        compilecommand = "g++ -std=c++11 {0} 2>compile_errors.txt".format(filename)
        os.system(compilecommand)
        if os.stat("compile_errors.txt").st_size:
            os.system("rm compile_errors.txt")
            return "CE"
        else:
            inputs = testcase + "input_"
            outputs = testcase + "output_"
            correct = 0
            for i in range(int(number)):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "timeout {1}s ./a.out < {0} > tempout.txt 2>runtime_errors.txt".format(inpi,timeout)
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                process = subprocess.Popen(command1, shell=True)
                process.communicate()
                retval=process.returncode
                if os.stat("runtime_errors.txt").st_size:
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt")
                    return 'RE'
                if retval==124:
                	os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt")
                	return 'TLE'
                os.system(command2)
                if os.stat("diff.txt").st_size == 0:
                    os.system("rm diff.txt")
                    correct += 1
                else:
                    os.system("rm a.out diff.txt tempout.txt compile_errors.txt runtime_errors.txt")
                    return "WA"
            os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt")
            return "AC"
    elif lang == 'py3':
        inputs = testcase + "input_"
        outputs = testcase + "output_"
        correct = 0
        for i in range(int(number)):
            inpi = inputs + str(i+1)
            outi = outputs + str(i+1)
            command1 = "timeout {2}s python3 {0} < {1} > tempout.txt 2>runtime_errors.txt".format(filename,inpi,timeout)
            command2 = "diff tempout.txt {0} > diff.txt".format(outi)
            process = subprocess.Popen(command1, shell=True)
            process.communicate()
            retval=process.returncode
            if os.stat("runtime_errors.txt").st_size:
                os.system("rm tempout.txt runtime_errors.txt")
                return 'RE'
            if retval==124:
                os.system("rm tempout.txt runtime_errors.txt")
                return 'TLE'
            os.system(command2)
            if os.stat("diff.txt").st_size == 0:
                os.system("rm diff.txt")
                correct += 1
            else:
                os.system("rm diff.txt tempout.txt runtime_errors.txt")
                return "WA"
        os.system("rm tempout.txt runtime_errors.txt")
        return "AC"
    elif lang == 'py':
        inputs = testcase + "input_"
        outputs = testcase + "output_"
        correct = 0
        for i in range(int(number)):
            inpi = inputs + str(i+1)
            outi = outputs + str(i+1)
            command1 = "timeout {2}s python {0} < {1} > tempout.txt 2>runtime_errors.txt".format(filename,inpi,timeout)
            command2 = "diff tempout.txt {0} > diff.txt".format(outi)
            process = subprocess.Popen(command1, shell=True)
            process.communicate()
            retval=process.returncode
            if os.stat("runtime_errors.txt").st_size:
                os.system("rm tempout.txt runtime_errors.txt")
                return 'RE'
            if retval==124:
                os.system("rm tempout.txt runtime_errors.txt")
                return 'TLE'
            os.system(command2)
            if os.stat("diff.txt").st_size == 0:
                os.system("rm diff.txt")
                correct += 1
            else:
                os.system("rm diff.txt tempout.txt runtime_errors.txt")
                return "WA"
        os.system("rm tempout.txt runtime_errors.txt")
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
            for i in range(int(number)):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "timeout {2}s java -cp {3} {0} < {1} > tempout.txt 2>runtime_errors.txt".format(os.path.basename(filei),inpi,timeout,os.path.dirname(filename))
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                os.system("echo "+command1+" > sample")
                process = subprocess.Popen(command1, shell=True)
                process.communicate()
                retval=process.returncode
                if os.stat("runtime_errors.txt").st_size:
                    os.system("rm "+filename[:-4]+"class tempout.txt compile_errors.txt runtime_errors.txt")
                    return 'RE'
                if retval==124:
                    os.system("rm "+filename[:-4]+"class tempout.txt compile_errors.txt runtime_errors.txt")
                    return 'TLE'
                os.system(command2)
                if os.stat("diff.txt").st_size == 0:
                    os.system("rm diff.txt")
                    correct += 1
                else:
                    os.system("rm diff.txt tempout.txt runtime_errors.txt "+filename[:-4]+"class")
                    return "WA"
            os.system("rm tempout.txt runtime_errors.txt "+filename[:-4]+"class")
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
            for i in range(int(number)):
                inpi = inputs + str(i+1)
                outi = outputs + str(i+1)
                command1 = "timeout {1}s ./a.out < {0} > tempout.txt 2>runtime_errors.txt".format(inpi,timeout)
                command2 = "diff tempout.txt {0} > diff.txt".format(outi)
                process = subprocess.Popen(command1, shell=True)
                process.communicate()
                retval=process.returncode
                if os.stat("runtime_errors.txt").st_size:
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt")
                    return 'RE'
                os.system(command2)
                if retval==124:
                    os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt")
                    return 'TLE'
                if os.stat("diff.txt").st_size == 0:
                    os.system("rm diff.txt")
                    correct += 1
                else:
                    os.system("rm a.out diff.txt tempout.txt compile_errors.txt runtime_errors.txt")
                    return "WA"
            os.system("rm a.out tempout.txt compile_errors.txt runtime_errors.txt")
            return "AC"
    else:
        return "no language found"
print(bashfunc(filename,testcase,number,lang,timeout))
