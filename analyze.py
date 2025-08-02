'''
given, version folder 
output inside version folder a test report 
in app dir i have known.txt so proccess that and keep in dict 

'''
import os 
class analyze:
    def __init__(self,versionDir) -> None:
        self.versionDir = versionDir
        self.currentDir = "./" + versionDir + "/"
    def proccessFile(self,pathToFile):
        '''
        Open known.txt with File as r 
        read line by line, save to list  
        return lst 
        '''
        ret = []
        try:
            with open(pathToFile, 'r') as file:
                for line in file:
                    ret.append(str(line.strip()).lower().lower().strip('"').strip("'"))
        except Exception as e:
            print(f"{pathToFile} bad {e}")
            return []
        return ret


    def countSubDir(self,currentDirectory):
        '''
        list = os module to ls currentDirectory
        return len(list)
        '''
        return [entry for entry in os.listdir(currentDirectory) if os.path.isdir(os.path.join(currentDirectory, entry))]
    def generateReport(self,version, totalErrors,knownErrors,newErors,table):
        '''
        output all the inputs to a file in the proper format
        if file: only add test name and table 
        '''
        '''
        table format: {testName: {device: {error: [numtimes,timestamp]} } }
        '''
        def tableFormat(fileLocal, table):
            '''
            table format: {device: {error: [numtimes,timestamp]} }
            '''
             
            for key in table:
                fileLocal.write(f"\n\nDevice {key}\n\n")
                temp = table.get(key)
                fileLocal.write("Error Name, Error Count, Timestamp\n\n")
                for key0 in temp:
                    fileLocal.write(f"{str(key0)}, {temp.get(key0)[0]}, {temp.get(key0)[1]}\n")

        try:
            with open((f"{self.currentDir}/test_report.txt"), 'w') as file:
                file.write(f"Version: {version}\n\n")
                file.write(f"Total {totalErrors} errors. Known {knownErrors}. New {newErors}")
                for key in table:
                    file.write(f"\n\n{str(key)}\n\n")
                    tableFormat(file,table.get(key))



        except Exception as e:
            raise Exception(e)
        


a1 = analyze("sw-v1")
knownLst = a1.proccessFile("./known.txt")
testDirs = a1.countSubDir(a1.currentDir)
reports = {} #{testName: {device:table} }
knownErrors = 0
newErrors = 0 
for testDir in testDirs:
    tempreport = {}
    deviceList = a1.countSubDir(a1.currentDir + testDir + "/")
    for i in range(len(deviceList)):
        perDeviceErrors = a1.proccessFile(f"{a1.currentDir}{testDir}/{deviceList[i]}/errors.txt")
        table = {} #{error: [numtimes,timestamp]}
        for error in perDeviceErrors:
            temp = error.split(",")
            timestamp = temp[0]
            errorMessage = temp[3].strip().strip('"').strip("'")
            if table.get(errorMessage) == None:
                table[errorMessage] = [1,timestamp]
            else:
                table.get(errorMessage)[0] +=1
            if str(errorMessage).lower() in knownLst:
                knownErrors+=1
            else:
                newErrors+=1
        tempreport[deviceList[i]] =  table
    reports[testDir] = tempreport
a1.generateReport(version=a1.versionDir, totalErrors=(knownErrors+newErrors),knownErrors=knownErrors,newErors=newErrors,table=reports) 


