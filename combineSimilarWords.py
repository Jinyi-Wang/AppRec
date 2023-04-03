from gensim.models import KeyedVectors
import numpy as np
from time import time
# gensim version: 4.2 x， 3.8 √

# combine similar words

rNo = 0

filePreTopic = open("testTopic.txt",'r',encoding='utf-8')
filePreTopicList = open("testTopic-list-2.txt",'r',encoding='utf-8')
filePreTopicListWrite = open("testTopic-list-3.txt",'w',encoding='utf-8')
filePreTopicWrite = open("testTopic-com.txt",'w',encoding='utf-8')


# 阈值x，目前设置为0.65。
line = filePreTopic.readline()
preTstring = ""
x = 0.65

# 0.6 638合并 0.65 573   0.7 532   0.75 505

# store topic and vec
comTopV = []
comTopN = []


# read corpus to get vectors
tic = time()
wv_from_text = KeyedVectors.load_word2vec_format("/mnt/TopicCombine/d100.txt", binary=False)
toc = time()
print('read embedding cost {:.2f}s'.format(toc - tic))

wv_from_text.init_sims(replace=True)


# read topic list列表，找到其向量，放入comTopV和comTopN
lineTL = filePreTopicList.readline()
while lineTL:
    preTstring = lineTL.strip()
    if preTstring in wv_from_text.wv.vocab.keys() :
        vec = wv_from_text[preTstring]
        comTopN.append(preTstring)
        comTopV.append(vec)
    lineTL = filePreTopicList.readline()
print("top len " + str(len(comTopV)))
tic = time()
print('read topic list {:.2f}s'.format(tic - toc))


cnt = 0
ticPre = time()
while line:
    cnt = cnt + 1
    if cnt % 10000 == 0 :
        ticNow = time()
        print(str(cnt / 10000) + "w lines has written..." + str(len(comTopV)))
        print('read tencent embedding cost {:.2f}s'.format(ticNow-ticPre))
        ticPre = time()
    line = line.strip()
    tmp = line.split("\t")
    # 空行是结尾，出循环
    if len(tmp) != 3:
        break
    else:
        # 拿到预备主题词，获取它的vec，如果可以拿到的话。
        preTstring = tmp[2]
        flag = 0
        if preTstring in wv_from_text.wv.vocab.keys() :
            vec1 = wv_from_text[preTstring]
            # 用预备主题的vec1和vec列表中的进行比较，如果相似度大于x，就合并过去，如果没有相似度大于x的，就放入vec列表
            for i in range(len(comTopV)):
                vec2 = comTopV[i]
                siml = cos_sim = vec1.dot(vec2) / np.linalg.norm(vec1) * np.linalg.norm(vec2)
                if siml > x:
                    flag = 1
                    # filePreTopicWriteLog.write(preTstring+"\t"+comTopN[i]+"\t"+str(siml)+"\n")
                    break
        else:
            # filePreTopicWriteLog2.write(preTstring+"\n")
            line = filePreTopic.readline()
            continue

        if flag == 1:
            filePreTopicWrite.write(tmp[0] + "\t" + tmp[1] + "\t" + comTopN[i] + "\n")
        else:
            comTopV.append(vec1)
            comTopN.append(preTstring)
            filePreTopicWrite.write(tmp[0] + "\t" + tmp[1] + "\t" + preTstring + "\n")
    line = filePreTopic.readline()

for k in range(len(comTopN)):
    filePreTopicListWrite.write(str(comTopN[k])+"\n")


filePreTopicWrite.close()
filePreTopic.close()
# filePreTopicWriteLog.close()
# filePreTopicWriteLog2.close()
filePreTopicList.close()
filePreTopicListWrite.close()


