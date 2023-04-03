# use stanford coreNLP in python: stanza

# pip install --index-url https://mirrors.aliyun.com/pypi/simple/ stanza


import stanza

import os
os.environ["STANZA_RESOURCES_DIR"] = "/mnt/stanza_resources"

fileReview = open("/mnt/data/post.txt",'r',encoding='utf-8')
fileReviewWrite = open("/mnt/data/topic/post.txt",'w',encoding='utf-8')

stanza.download('zh') # download English/Chinese model
nlp = stanza.Pipeline('zh', processors='tokenize,pos') # initialize English neural pipeline

cnt = 0
appid = ""
userid = ""
line = fileReview.readline()
while line:
    # 如果该行是appid，保存到appid里
    if(line[0:2] == "#*"):
        appid = line[2:].strip()
    # 如果该行是userid，保存到userid里
    if (line[0:2] == "#@"):
        userid = line[2:].strip()
    # 如果该行是用户发表的内容，那么进行topic提取--
    if(line[0:2] == "#!"):
        # 输出一个计数
        if(cnt%100==0):
            print(str(cnt))        #count how many post have processed
        cnt = cnt + 1

        review = line[2:]
        doc = nlp(review) # run annotation over a sentence
        for sentence in doc.sentences:
            #  topic词选择VERB NOUN ADJ
            for word in sentence.words:
                if (word.upos == "VERB" or word.upos == "NOUN" or word.upos == "ADJ"):
                    fileReviewWrite.write("a_"+appid+'\t'+"u_"+userid+'\t'+str(word.text)+'\n')
    line = fileReview.readline()

fileReview.close()
fileReviewWrite.close()
