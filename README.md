# AppRec

Some of the codes in my research.   
My research aims to recommend mobile applications for users. 


## crawler.py
Crawl data of user, app, reviews and posts.   
It includes user's behavioral information(time consumption of using apps, and forum level) and published information(contents of reviews and posts).

## extractTopic.py
Extract nouns, verbs and adjs from natural texts.   
Using NLP toolkit.

## combineSimilarWords.py
Use corpus to combine similar words.    
These words are extracted from different reviews/posts.

## recMultiMetagraph.py
Input: node vecters from different embedding(user's node and app's node), test set.   
Output: recommendations for each user.

## evalResult.py
Evalute the recommendation results.    
Metrics: P R F1 NDCG.

