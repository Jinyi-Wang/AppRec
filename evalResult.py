import numpy as np
from sklearn.metrics import roc_auc_score

def eval(tru,pre): #input: truth set and prediction set
    precision = 0
    recall = 0

    stru = set(tru)
    spre = set(pre)

    # use set to calculate P R F1
    if len(spre)!=0:
        intersection = [i for i in tru if i in spre] #求交集
        inter = set(intersection)

        recall = len(inter) / len(stru)
        precision = len(inter) / len(spre)

    if precision == 0 or recall == 0:
        f1 = 0
    else:
        f1 = 2*precision*recall /(precision+recall)

    # calculate rel and NDCG  if index N is true, rel[N] = 1
    k = len(pre)
    pred_rel = [0] * k
    for i in range(k):
        if pre[i] in stru:
            pred_rel[i] = 1
        else:
            pred_rel[i] = 0

    dcg = 0
    for (index, rel) in enumerate(pred_rel):
        dcg += (rel * np.reciprocal(np.log2(index + 2)))
    idcg = 0
    for (index, rel) in enumerate(sorted(pred_rel, reverse=True)):
        idcg += (rel * np.reciprocal(np.log2(index + 2)))

    if idcg == 0:
        ndcg = 0
    else:
        ndcg =  dcg / idcg

    return precision,recall,f1,ndcg


def hit(gt_items, pred_items):
    count = 0
    for item in pred_items:
        if item in gt_items:
            count += 1
    return count

# 对于推荐列表中的每一项i，如果在gt里面，就计入1/i。把推荐列表全部看一遍，得到总数作为mrr值。
def mrr(gt_items, pred_items):
    count = 0.0
    for index,item in enumerate(pred_items):
        if item in gt_items:
            count += 1/(index+1)
    return count


if __name__ == "__main__":

    filePath = '../testData/sim-'

    fileact = open("../testData/tap-uat0.txt", 'r', encoding='utf-8')

    filerec = open("../testData/upapu-rec.txt", 'r', encoding='utf-8')
    fileeval = open("../testData/upapu-eval.txt", 'w', encoding='utf-8')


    clearNo = 300000
    # top K
    K = [5, 10, 20, 30, 50]

    # userList里的user出现顺序和ua0一致(actList和recList出现的顺序是一致的)
    userList = []
    recList = [[] * 0 for row in range(clearNo)]
    actList = [[] * 0 for row in range(clearNo)]

    cnt = 0
    # 读取文件uat0 rec，放到两个矩阵里面。
    line = filerec.readline()
    while line:
        temp = line.split("\n")
        temp = temp[0].split("\t")
        userName = temp[0]
        userIndex = userList.index(userName) if userName in userList else -1
        if (userIndex == -1):
            userList.append(userName)
            userIndex = userList.index(userName)
        recList[userIndex].append(temp[1])
        cnt = cnt + 1
        if (cnt % 10000 == 0):
            print(cnt)
        line = filerec.readline()

    print("recList and appList over!")

    cnt = 0
    line = fileact.readline()
    while line:
        temp = line.split("\n")
        temp = temp[0].split("\t")
        userName = temp[0]
        userIndex = userList.index(userName) if userName in userList else -1
        if (userIndex == -1):
            print("User in act not in rec, delete!" + userName)
            line = fileact.readline()
            continue
        # simList是三维数组，temp存入数组['a_220021', '0.9362813730238934']……
        actList[userIndex].append(temp[1])
        cnt = cnt + 1
        if (cnt % 10000 == 0):
            print(cnt)
        line = fileact.Freadline()

    print("actList over!")

    fileeval.write("userNo" + str(len(userList)))
    for k in K:
        fileeval.write("\n \nk = " + str(k) + "\n")
        count = 0
        sump = 0.0
        sumr = 0.0
        sumf = 0.0
        sumn = 0.0
        sumhits = 0.0
        sumMrr = 0.0
        lentru = 0
        cnt = 0
        for i in range(0, clearNo):
            cnt = cnt + 1
            if (cnt % 10000 == 0):
                print(cnt)
            if len(recList[i]) == 0 or len(actList[i]) == 0:
                break
            tru = actList[i]
            pre = recList[i][0:k]

            # 计算hitRate的函数
            hits = hit(tru, pre)
            lentru = lentru + len(tru)

            # 计算MRR
            mrr0 = mrr(tru, pre)

            # if use set, NDCG will not calculate correctly, so use list
            p, r, f, n = eval(tru, pre)
            sump = sump + p
            sumr = sumr + r
            sumf = sumf + f
            sumn = sumn + n
            sumhits = sumhits + hits
            sumMrr = sumMrr +mrr0
            count = count + 1

        # hitRate
        hitRate = sumhits/lentru

        print(k)
        print(sump, sumr, sumf, sumn, hitRate, sumhits, lentru, sumMrr)
        print(count)
        fileeval.write(str(sump) + "\t" + str(sumr) + "\t" + str(sumf) + "\t" + str(sumn) + '\t'
                       + str(hitRate) + '\t'+ str(sumhits) + '\t'+ str(lentru) + '\t'+ str(sumMrr)
                       + '\n')
        fileeval.write('count = ' + str(count) + '\n')

    filerec.close()
    fileact.close()
    fileeval.close()




