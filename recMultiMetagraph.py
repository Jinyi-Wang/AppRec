

# Make recommendations, using results acquired by differnet metagraphs
# Delete intersection with used apps in test files


# different weights
a2 = 0
a3 = 0
a4 = 0
a5 = 0
a6 = 1
a7 = 1


# uauValue,uatuValue,uafuValue,upapuValue,uraruValue

# Using different weights to calculate the scores
def calRec(uatuV, uafuV, upapuV, uraruV, upuV, uruV):
    res = uatuV * a2 + uafuV * a3 + upapuV * a4 + uraruV * a5 + upuV * a6 + uruV * a7
    return res

# file Read(u a sim)， put into inputList
def readFile(fileRead, inputList, userList):
    cnt = 0
    line = fileRead.readline()
    while line and line != '\n':
        # user from line, user id from userList
        temp = line.split("\n")
        temp = temp[0].split(" ")
        userName = temp[0]
        userIndex = userList.index(userName) if userName in userList else -1
        if (userIndex == -1):
            # new users. Not in test set(80/20). The user use less than five apps
            line = fileRead.readline()
            continue

        # inputList is three-dimensional array，temp eg.['a_220021', '0.9362813730238934']……
        temp.pop(0)
        inputList[userIndex].append(temp)
        # inputList appname
        # inputList[userIndex].append(temp[1])
        cnt = cnt + 1
        if (cnt % 10000 == 0):
            print(' line: '+str(cnt))
        line = fileRead.readline()


if __name__ == "__main__":

    filePath = '../testData/sim-'
    fileAppPath = "../testData/tap-uagt0.txt"

    filerec = open(filePath +str(a1) +str(a2) +str(a3) +str(a4) +str(a5) +str(a6) +str(a7) +".txt", 'w', encoding='utf-8')

    # read  user used app lists: fileuse
    fileapp = open(fileAppPath, 'r', encoding='utf-8')
    # read vectors obtained by each walking
    fileuatu = open(filePath + "uatu.txt", 'r', encoding='utf-8')
    fileuafu = open(filePath + "uafu.txt", 'r', encoding='utf-8')
    fileuraru = open(filePath + "uraru.txt", 'r', encoding='utf-8')
    fileupapu = open(filePath + "upapu.txt", 'r', encoding='utf-8')
    fileupu = open(filePath + "upu.txt", 'r', encoding='utf-8')
    fileuru = open(filePath + "uru.txt", 'r', encoding='utf-8')

    # userList and test file, have same users
    # read users into userList
    userList = []
    line = fileapp.readline()
    while line:
        temp = line.split("\n")
        temp = temp[0].split("\t")
        userName = temp[0]
        userIndex = userList.index(userName) if userName in userList else -1
        if (userIndex == -1):
            userList.append(userName)
            userIndex = userList.index(userName)
        line = fileapp.readline()
    fileapp.close()

    print("userlist get")
    clearNo = len(userList)

    # store
    appList = [[] * 0 for row in range(clearNo)]
    uauList = [[] * 0 for row in range(clearNo)]
    uatuList = [[] * 0 for row in range(clearNo)]
    uafuList = [[] * 0 for row in range(clearNo)]
    upapuList = [[] * 0 for row in range(clearNo)]
    uraruList = [[] * 0 for row in range(clearNo)]
    upuList = [[] * 0 for row in range(clearNo)]
    uruList = [[] * 0 for row in range(clearNo)]

    # read files of vectors and user-app relationship, and store them
    readFile(fileuatu,uatuList,userList)
    readFile(fileuafu,uafuList,userList)
    readFile(fileuraru,uraruList,userList)
    readFile(fileupapu,upapuList,userList)
    readFile(fileupu,upuList,userList)
    readFile(fileuru,uruList,userList)
    print("lists get")

    # actual used situation -- appList
    fileapp1 = open(fileAppPath, 'r', encoding='utf-8')
    cnt = 0
    line = fileapp1.readline()
    while line and line != '\n':
        # user from line, id from userList
        temp = line.split("\n")
        temp = temp[0].split("\t")
        userName = temp[0]
        userIndex = userList.index(userName) if userName in userList else -1
        if (userIndex == -1):
            line = fileapp1.readline()
            continue

        appList[userIndex].append(temp[1])
        cnt = cnt + 1
        if (cnt % 10000 == 0):
            print(' line: ' + str(cnt))
        line = fileapp1.readline()
    print("fileapp over!")

    simList = [[] * 0 for row in range(clearNo)]

    # put recommend results into simList
    for i in range(0,len(userList)):
        uauDict = {}
        uatuDict = {}
        uafuDict = {}
        uraruDict = {}
        upapuDict = {}
        upuDict = {}
        uruDict = {}
        sumDict = {}
        aList = []

        # uauList[i] = [ ['a','sim'], ['a','sim'], ... ]
        # put similarities into dicts, remember app names
        for j in range(0, len(uatuList[i])):
            aList.append(uatuList[i][j][0])
            uatuDict[uatuList[i][j][0]] = float(uatuList[i][j][1])
        for j in range(0, len(uafuList[i])):
            aList.append(uafuList[i][j][0])
            uafuDict[uafuList[i][j][0]] = float(uafuList[i][j][1])
        for j in range(0, len(uraruList[i])):
            aList.append(uraruList[i][j][0])
            uraruDict[uraruList[i][j][0]] = float(uraruList[i][j][1])
        for j in range(0, len(upapuList[i])):
            aList.append(upapuList[i][j][0])
            upapuDict[upapuList[i][j][0]] = float(upapuList[i][j][1])
        for j in range(0, len(upuList[i])):
            aList.append(upuList[i][j][0])
            upuDict[upuList[i][j][0]] = float(upuList[i][j][1])
        for j in range(0, len(uruList[i])):
            aList.append(uruList[i][j][0])
            uruDict[uruList[i][j][0]] = float(uruList[i][j][1])
        aList = list(set(aList))

        # rec with values
        for k in range(0,len(aList)):
            uatuValue = uatuDict.get(aList[k]) if aList[k] in uatuDict else 0
            uafuValue = uafuDict.get(aList[k]) if aList[k] in uafuDict else 0
            uraruValue = uraruDict.get(aList[k]) if aList[k] in uraruDict else 0
            upapuValue = upapuDict.get(aList[k]) if aList[k] in upapuDict else 0
            upuValue = upuDict.get(aList[k]) if aList[k] in upuDict else 0
            uruValue = uruDict.get(aList[k]) if aList[k] in uruDict else 0
            sumValue = calRec(uatuValue,uafuValue,upapuValue,uraruValue,upuValue,uruValue)
            if sumValue != 0:
                sumDict[aList[k]] = sumValue

        # sort dict and put into recList
        sumDict = sorted(sumDict.items(), key=lambda item: item[1],reverse=True)
        for k in range(0,len(sumDict)):
            simList[i].append(sumDict[k][0])

    # pop used apps, rec new apps to users
    cnt = 0
    for i in range(0,clearNo):
        if simList[i] == []:
            continue
        for j in range(0,len(appList[i])):
            appName = appList[i][j]
            appIndex = simList[i].index(appName) if appName in simList[i] else -1
            if appIndex != -1:
                print("used app! "+appName+" "+str(cnt))
                cnt = cnt+1
                simList[i].pop(appIndex)
    print("pop used app over! ")

    # output rec results
    topk = 150
    for i in range(0, clearNo):
        if simList[i] == []:
            continue
        userName = userList[i]
        len1 = len(simList[i])
        if len1 > topk:
            len1 = topk
        for j in range(0,len1):
            filerec.write( userName +"\t"+ simList[i][j] + "\n")
    print("First topk app for each user store over! topk = "+str(topk))
    filerec.close()

    fileuatu.close()
    fileuafu.close()
    fileuraru.close()
    fileupapu.close()
    fileupu.close()
    fileuru.close()
    fileapp1.close()


