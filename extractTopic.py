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
    # appid
    if(line[0:2] == "#*"):
        appid = line[2:].strip()
    # userid
    if (line[0:2] == "#@"):
        userid = line[2:].strip()
    # content of reviews/posts
    if(line[0:2] == "#!"):
        # count
        if(cnt%100==0):
            print(str(cnt))        #count how many reviews/posts have processed
        cnt = cnt + 1

        review = line[2:]
        doc = nlp(review) # run annotation over a sentence
        for sentence in doc.sentences:
            #  chose VERB NOUN ADJ as topic words
            for word in sentence.words:
                if (word.upos == "VERB" or word.upos == "NOUN" or word.upos == "ADJ"):
                    fileReviewWrite.write("a_"+appid+'\t'+"u_"+userid+'\t'+str(word.text)+'\n')
    line = fileReview.readline()

fileReview.close()
fileReviewWrite.close()
