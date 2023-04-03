import json
import time
import re
import requests
import xlwt

# It is a crawler which could crawl data from taptap.com
# It worked in Nov 2021, and the site maybe change a little now.


# page number of reviews and posts crawling
reviewNo = 100
postNo = 100

# app's index
beginNo = 1
endNo = 150


# get user data
def getUserData(fileUser, userid):
    # user's basic interface
    params = {
        'id': userid,
        'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=43&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
    }
    response = requests.get('https://www.taptap.com/webapiv2/user/v1/detail', headers=headers, params=params,
                             proxies=proxies)
    userDetailed = json.loads(response.text)

    # write user's data
    fileUser.write('#@'+str(userDetailed['data']['id']) + '\n')  # id
    fileUser.write('#!' + userDetailed['data']['name'] + '\n')  # nickname
    fileUser.write('#i' +userDetailed['data']['intro'] + '\n')  # intro
    fileUser.write('#' +str(userDetailed['data']['stat']['fans_count']) + '\n')  # fans number
    fileUser.write('#d' +str(userDetailed['data']['stat']['created_days']) + '\n')  # created days
    fileUser.write('#t' +str(userDetailed['data']['stat']['created_moment_count']) + '\n')  # "图文", moment number
    fileUser.write('#r' +str(userDetailed['data']['stat']['created_review_count']) + '\n')
    fileUser.write('#p' +str(userDetailed['data']['stat']['created_post_count']) + '\n')  # "长帖", post number
    fileUser.write('#y' +str(userDetailed['data']['stat']['played_count']) + '\n')  # number of played games
    fileUser.write('#s' +str(userDetailed['data']['stat']['played_spent']) + '\n')  # total played time
    fileUser.write('#u' +str(userDetailed['data']['stat']['voteup_count']) + '\n')  # total likes acquired

    # followed interface to read app info
    # all followed apps, 10 apps/page
    i = 0
    while 1:
        params = {
            'from': str(i * 10),
            'limit': 10,
            'type': 'app',
            'user_id': userid,
            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
        }
        response = requests.get('https://www.taptap.com/webapiv2/friendship/v1/following-by-user', headers=headers,
                                params=params, proxies= proxies)
        dataApp = json.loads(response.text)
        dataAppList = dataApp['data']['list']
        for k in dataAppList:
            fileUser.write('#f' +str(k['id']) + '\n')
        i = i + 1
        if len(dataApp['data']['next_page']) == 0:
            break

    # time consumption for each app
    followedApp = userDetailed['data']['stat']['following_app_count']  # followed numbers
    # 10 apps/page
    i = 0
    while 1:
        params = {
            'user_id': userid,
            'limit': 10,
            'from': str(i * 10),
            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
        }
        response = requests.get('https://www.taptap.com/webapiv2/user-app/v1/user-spent-list',
                                headers=headers, params=params, proxies=proxies)
        dataApp = json.loads(response.text)
        dataAppList = dataApp['data']['list']
        for k in dataAppList:
            fileUser.write('#m' +str(k['app']['id']) + ' ' + str(k['spent']) + '\n')
        i = i + 1
        if len(dataApp['data']['next_page']) == 0:
            break

    # forum interface to get forum data
    # 10 forums/page
    i = 0
    while 1:
        params = {
            'user_id': userid,
            'limit': 10,
            'from': str(i * 10),
            # here a time stamp, should update
            'max_updated_at': '2021-10-28 19:18:29',
            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
        }
        if i == 0:
            params = {
                'user_id': userid,
                'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
            }
        response = requests.get('https://www.taptap.com/webapiv2/forum-level/v1/by-user',
                                headers=headers, params=params, proxies=proxies)
        dataApp = json.loads(response.text)
        dataAppList = dataApp['data']['list']
        if len(dataAppList) == 0:
            break
        for k in dataAppList:
            fileUser.write('#l' + str(k['app_id']) + ' ' + str(k['level']['level']) + '\n')
        i = i + 1
        if len(dataApp['data']['next_page']) == 0:
            break
    fileUser.write('\n')
    print("user id:" + str(userid))


# get 150 apps in popular lists
# store app id into appList
def getAppList(fileAppList, appList):
    for i in range(0, 10):
        params = {
            'platform': 'android',
            'type_name': 'pop',
            'limit': '15',
            'from': str(15 * i),
            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
        }
        response = requests.get('https://www.taptap.com/webapiv2/app-top/v1/hits', headers=headers, params=params,
                                proxies=proxies)
        data = json.loads(response.text)
        for j in range(0, 15):
            appList.append(data['data']['list'][j]['id'])
            fileAppList.write(str(data['data']['list'][j]['id']) + ' ' + data['data']['list'][j]['title'] + '\n')


# get details of each app
def getAppData(appId, fileApp):
    params = (
        ('X-UA',
         'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC'),
    )
    response = requests.get('https://www.taptap.com/webapiv2/app/v2/detail-by-id/' + str(appId),
                            headers=headers, params=params, proxies=proxies)
    dataDetail = json.loads(response.text)

    # details
    fileApp.write('#@' + dataDetail['data']['title'] + '\n')
    fileApp.write('#$' + str(appId) + '\n')
    fileApp.write('#f' + str(dataDetail['data']['stat']['fans_count']) + '\n')  # followed number
    fileApp.write('#d' + str(dataDetail['data']['stat']['hits_total']) + '\n')  # downloads number
    fileApp.write('#r' + str(dataDetail['data']['stat']['review_count']) + '\n')  #
    fileApp.write('#a' + str(dataDetail['data']['stat']['rating']['score']) + '\n')  # rates
    fileApp.write('#!' + str(dataDetail['data']['description']['text']) + '\n')
    if dataDetail['data'].get('highlight_tags', []) != []:  # rank in different lists
        for tag in dataDetail['data']['highlight_tags']:
            if tag['type'] == 'editors_choice':
                fileApp.write('#h' + '编辑推荐' + '\n')
            elif tag['type'] == 'exclusive':
                continue
            else:
                fileApp.write('#h' + tag['data']['label'] + '\n')

    for item in dataDetail['data']['stat']['review_tags']['mappings']:
        fileApp.write('#%' + str(item['mapping']) + ' ' + str(item['label']) + '\n')  # tag in reviews(features) and emotions(+/-)
    for item in dataDetail['data']['tags']:
        fileApp.write('#c' + str(item['value']) + '\n')  # category
    fileApp.write('\n')
    print("data details finished："+str(appId)+': '+dataDetail['data']['title']+'\n')

# replies and likes up to 100 person/review. (max 7000+ repies to one review)
def getReviewData(appId,fileReview,userList):
    # review
    reviewList = []
    # get reviewNo*10 replies
    for i in range(0, reviewNo):
        params = {
            'app_id': str(appId),
            'limit': '10',
            'from': str(i * 10),
            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
        }
        if i == 0:
            params = {
                'app_id': str(appId),
                'limit': '10',
                'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
            }
        response = requests.get('https://www.taptap.com/webapiv2/review/v2/by-app', headers=headers, params=params,
                                proxies=proxies)
        dataReview = json.loads(response.text)
        dataReviewList = dataReview['data']['list']
        if dataReviewList == []:
            break
        # read details of each review
        for j in range(0, len(dataReviewList)):
            print(str(appId)+'No. ' + str(i * 10 + j + 1) + 'review'+str(i)+str(j))

            userid = dataReview['data']['list'][j]['moment']['author']['user']['id']
            userList.append(userid)
            reviewid = dataReview['data']['list'][j]['moment']['extended_entities']['reviews'][0]['id']

        # write
            fileReview.write( '#@' + str(userid)+ '\n')
            fileReview.write( '#*' + str( dataReview['data']['list'][j]['moment']['app']['id']) + '\n')
            fileReview.write( '#!' + str( dataReview['data']['list'][j]['moment']['extended_entities']['reviews'][0]['contents'][
                    'text']) + '\n')
            fileReview.write( '#u' + str( dataReview['data']['list'][j]['moment']['stat']['ups']) + '\n')
            fileReview.write( '#d' + str( dataReview['data']['list'][j]['moment']['stat']['downs']) + '\n')
            fileReview.write( '#q' + str( dataReview['data']['list'][j]['moment']['stat']['comments']) + '\n')
            fileReview.write( '#r' + str( dataReview['data']['list'][j]['moment']['extended_entities']['reviews'][0]['score']) + '\n')

            # replies
            k = 0
            while 1:
                params = {
                    'order': 'asc',
                    'show_top': 1,
                    'review_id': str(reviewid),
                    'limit': 10,
                    'from': str(k * 10),
                    'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                }

                '''params = {
                    'review_id': reviewList[k]['reviewId'],
                    'order': 'asc',
                    'show_top': 1,
                    'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                }'''

                response = requests.get('https://www.taptap.com/webapiv2/review-comment/v1/by-review', headers=headers,
                                        params=params,
                                        proxies=proxies)
                dataRev = json.loads(response.text)
                dataRevList = dataRev['data']['list']
                for rev in dataRevList:
                    fileReview.write('#l' + str(rev['author']['id']) + '\n')
                    fileReview.write('#y' + str(rev['contents']['text']) + '\n')
                    fileReview.write('#+' + str(rev['ups']) + '\n')
                k = k + 1
                if len(dataRev['data']['next_page']) == 0 or k >= 10:
                    break

            # likers's id
            k = 0
            while 1:
                params = {
                    'from': 0,
                    'id': 'review:' + str(reviewid),
                    'limit': 10,
                    'from': str(k * 10),
                    'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                }
                if k == 0:
                    params = {
                        'id': 'review:' + str(reviewid),
                        'from': 0,
                        'limit': 10,
                        'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                    }

                response = requests.get('https://www.taptap.com/webapiv2/vote/v1/by-object', headers=headers,
                                        params=params,
                                        proxies=proxies)
                dataRev = json.loads(response.text)
                dataRevList = dataRev['data']['list']
                for rev in dataRevList:
                    fileReview.write('#p' + str(rev['id']) + '\n')

                k = k + 1
                if len(dataRev['data']['next_page']) == 0 or k >= 10:
                    break
            fileReview.write('\n')


# forum
def getPostData(appId,filePost,userList):
    params = {
        'app_id': str(appId),
        'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
    }
    response = requests.get('https://www.taptap.com/webapiv2/group/v1/detail', headers=headers, params=params,
                            proxies=proxies)
    dataApp = json.loads(response.text)
    forumId = dataApp['data']['group']['id']

    # 10 forums/page
    for i in range(0, postNo):
        params = {
            'group_id': str(forumId),
            'sort': 'commented',
            'type': 'feed',
            'limit': '10',
            'from': str(i * 10),
            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
        }
        response = requests.get('https://www.taptap.com/webapiv2/feed/v6/by-group', headers=headers, params=params,
                                proxies=proxies)
        dataReview = json.loads(response.text)
        dataReviewList = dataReview['data']['list']
        if dataReviewList == []:
            break

        # three types in the forum: moment, post, video
        for j in range(0, len(dataReviewList)):
            print(str(appId)+'第' + str(i * 10 + j + 1) + '条post')
            # moment id, post id
            postId = dataReviewList[j]['moment']['event_log']['paramId']
            momentId = dataReviewList[j]['moment']['id']
            type = dataReviewList[j]['moment']['event_log']['paramType']

            # with a topic, it is a post
            if type == 'topicDetail':
                params = {
                    'id': str(postId),
                    'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                }
                response = requests.get('https://www.taptap.com/webapiv2/topic/v1/detail', headers=headers,
                                        params=params,
                                        proxies=proxies)
                dataPost = json.loads(response.text)
                filePost.write('#@' + str(dataPost['data']['first_post']['author']['id']) + '\n')
                userList.append(dataPost['data']['first_post']['author']['id'])
                filePost.write('#*' + str(appId) + '\n')
                content = str(dataPost['data']['topic']['title']) + '    ' + dataPost['data']['first_post']['contents']['text'] # title + content
                filePost.write('#!' + content + '\n')
                filePost.write('#q' + str(dataPost['data']['topic']['comments']) + '\n')  # relies number
                filePost.write('#u' + str(dataPost['data']['topic']['ups']) + '\n')  # likes number
                filePost.write('#k' + str(dataPost['data']['topic']['stat']['pv_total']) + '\n')  # Number of scans

                if dataPost['data']['topic']['comments'] != 0:
                    # reply details
                    k = 0
                    while 1:
                        params = {
                            'from': str(k * 10),
                            'limit': '10',
                            'topic_id': str(postId),
                            'sort': 'position',
                            'order': 'asc',
                            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                        }
                        response = requests.get('https://www.taptap.com/webapiv2/post/v3/by-topic', headers=headers,
                                                params=params, proxies=proxies)
                        feedbackList = json.loads(response.text)
                        for feedback in feedbackList['data']['list']:
                            filePost.write('#l' + str(feedback['author']['id']) + '\n')
                            filePost.write('#y' + feedback['contents']['text'] + '\n')
                            filePost.write('#+' + str(feedback['ups']) + '\n')
                        k = k + 1
                        if (len(feedbackList['data']['next_page']) == 0) or k >= 10:
                            break

                if dataPost['data']['topic']['ups'] != 0:
                    # like details
                    k = 0
                    while 1:
                        params = {
                            'id': 'topic:' + str(postId),
                            'from': str(k * 10),
                            'limit': '10',
                            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                        }
                        response = requests.get('https://www.taptap.com/webapiv2/vote/v1/by-object', headers=headers,
                                                params=params, proxies=proxies)
                        feedbackList = json.loads(response.text)
                        for feedback in feedbackList['data']['list']:
                            filePost.write('#p' + str(feedback['id']) + '\n')
                        k = k + 1
                        if (len(feedbackList['data']['next_page']) == 0) or k >= 10:
                            break

            # without a topic, it is a moment
            elif type == 'momentDetail':
                params = {
                    'id': str(postId),
                    'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                }
                response = requests.get('https://www.taptap.com/webapiv2/moment/v2/detail', headers=headers,
                                        params=params,
                                        proxies=proxies)
                dataPost = json.loads(response.text)
                filePost.write('#@' + str(dataPost['data']['moment']['author']['user']['id']) + '\n')
                userList.append(dataPost['data']['moment']['author']['user']['id'])
                filePost.write('#*' + str(appId) + '\n')
                filePost.write('#!' + dataPost['data']['moment']['contents']['text'] + '\n')
                filePost.write('#k' + str(dataPost['data']['moment']['stat']['pv_total']) + '\n')  # 浏览数
                filePost.write('#u' + str(dataPost['data']['moment']['stat']['ups']) + '\n')  # 数
                filePost.write('#q' + str(dataPost['data']['moment']['stat']['comments']) + '\n')  # 数

                # replies
                if dataPost['data']['moment']['stat']['comments'] != 0:
                    k = 0
                    while 1:
                        params = {
                            'id': str(postId),
                            'order': 'asc',
                            'show_top': '1',
                            'regulate_all': '0',
                            'from': str(k * 10),
                            'limit': '10',
                            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                        }
                        if k == 0:
                            params = {
                                'id': str(postId),
                                'order': 'asc',
                                'show_top': '1',
                                'regulate_all': '0',
                                'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                            }
                        response = requests.get('https://www.taptap.com/webapiv2/comment/v1/by-object', headers=headers,
                                                params=params, proxies=proxies)

                        # reply details
                        feedbackList = json.loads(response.text)
                        for feedback in feedbackList['data']['list']:
                            filePost.write('#l' + str(feedback['author']['user']['id']) + '\n')
                            filePost.write('#y' + feedback['contents']['text'] + '\n')
                            filePost.write('#+' + str(feedback['stat']['ups']) + '\n')
                        k = k + 1
                        if (len(feedbackList['data']['next_page']) == 0) or k >= 10:
                            break

                # like details
                if dataPost['data']['moment']['stat']['ups'] != 0:
                    k = 0
                    while 1:
                        params = {
                            'id': 'moment:' + str(postId),
                            'from': str(k * 10),
                            'limit': '10',
                            'X-UA': 'V=1&PN=WebApp&LANG=zh_CN&VN_CODE=42&VN=0.1.0&LOC=CN&PLT=PC&DS=Android&UID=324eeff8-0927-46c2-8d9f-367da69d9fef&DT=PC',
                        }
                        response = requests.get('https://www.taptap.com/webapiv2/vote/v1/by-object', headers=headers,
                                                params=params, proxies=proxies)
                        feedbackList = json.loads(response.text)
                        for feedback in feedbackList['data']['list']:
                            filePost.write('#p' + str(feedback['id']) + '\n')
                        k = k + 1
                        if (len(feedbackList['data']['next_page']) == 0) or k >= 10:
                            break



# transform list into str
def listToStr(list):
    listNew = []
    if len(list) > 10:
        list = list[0:10]

    if len(list) > 1:
        for i in range(0, len(list)):
            if len(list[i]) < 100:
                listNew.append(list[i])

    elif len(list) == 1 and len(list[0]) > 100:
        del (list[0])

    str = ''
    for item in listNew:
        if item == listNew[-1]:
            str = str + item
        else:
            str = str + item + '|'
    return str


if __name__ == '__main__':
    # define cookie,headers
    cookies = {
        'tapadid': '393bd9c6-2c34-ae22-fee2-165c7e64bd97',
        '_ga': 'GA1.2.1971225269.1631459785',
        'ssxmod_itna': 'QqUx9D2iitDQi=5GHD8ibmOAGDO/W1Nb18bNDlhioxA5D8D6DQeGTb2WDBnY6ClAxxWx5iShhKfAiro+aYWcry07SiOa+toDU4i8DCki5QmxeW=D5xGoDPxDeDADYo0DAqiOD7dtDEDmRkDGeDeZF8DY5DhxDCXBPDwx0CXcWqXrAHY+5m9=DhNZKD9ooDsZiEHRAEA90sAmKDXPdDvE5zXa5mDB4oWGb5jlP7DiFjDC5pcDDaXhiqM9DDMl90KixcDGycbnwbZQGKqAuDd704Hnx4TZii=itK2srqDDcuEMwDD=',
        'XSRF-TOKEN': 'eyJpdiI6ImhZWWRwNzRlbExObENaUit2Sm5UVmc9PSIsInZhbHVlIjoiR1pjUnB1b2hnRUlZT1wvSnMybDIrNXVhUlQ5YlZyRHI2Z2wyUHVtenFwSUNoYjNqUHM2SW9YRnhIbVFPQUlLYVk1SUJ1SnZrODQ1cWFVemxuYXNHWDJRPT0iLCJtYWMiOiIxNDBlZGI3ODg3OWJhODE0MWVlNWFiZjZjNDY4NTQ5NTE0ZGE0ZWZjODE1ZDJlODZhMjRkZTgyMGUyOGU3NjVjIn0%3D',
        'tap_sess': 'eyJpdiI6Ik5YdlJMNmY3bzRLQzd1OVk2M2J0ZkE9PSIsInZhbHVlIjoiYWNCY0gyWjRWVHZ6Y1YxS1A1ODQ5UVBzU3lNNGg5YWRaajZ5eFFBNk0wMzRFTTNHRG10cGx3VmtVdElqbGRlTmVaZ2dLOHJzanV4ZmFNV3JKXC9xdmZnPT0iLCJtYWMiOiIzNzZjYjlhY2ViNmY3ZTNmYjQ0ZDVlNjMwNTdjOWEwZDdiNmZjMjJlZTkxOTJmNTNjMTQyMTczY2Y0YmE2YTA4In0%3D',
        '_uab_collina': '163167046264514576220711',
        '_gid': 'GA1.2.1736614628.1631670463',
        '_ga_6G9NWP07QM': 'GS1.1.1631704077.7.0.1631704084.0',
        'ssxmod_itna2': 'QqUx9D2iitDQi=5GHD8ibmOAGDO/W1Nb18D6O+jY4054aTq031WqRYcWKWjD6nhIj5VzQe5rsyAGu0Xx1IhD8TDB0ffQsOAxcp9ktqSwOtFylp=qF6YmbGPTsd0x5=14ZCT5AQkSETfxCOjkQuAy7o36Ak=eiidcC4ReuRv5483v9RYqMOdObeTOAdee72YwI3tV8brOQeUG3uoEfLA98QeFIxWqz70zq4UzdMTYaSFiMThsjn=bkB532rSmx1=R8TOw7zukbeYmuCGPItWCSBCXVoYE9CjQhwQ4nfqoyeOYTRD63kisWXmp6/=0go5gctZaIY0dMpUcxEHjU76UQpX5IxccvDS55+6LQGUchpixB7owBmUgEHoP+ndotN4ANoFPLhKozf/YpNa0Q62EAPwlhsY0Q13n0iua0knx1/AY=wlc6Gzp6BD8iv5ja=0+S=Dc7aYOqmBjjfjGYEvifnZoT4L/PpNcoOmNInXI6pMS3Z9flKH/bxwlNLStCCj6hD+i96YNZGU5nqkoIKgoEcnfg+/E3vivQ1PAbd9C2BQ3GWIt7UPgw=w3fFOTDG2RrabZEG9wYiZWj8Uv61rtc=bR+xD08DiQEcD8woccDrRd70LQCfKn+v5QeWkHiDxD',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22411771879%22%2C%22%24device_id%22%3A%2217be726848d333-0c313ba91db70e8-4c3e2778-3686400-17be726848e907%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217be726848d333-0c313ba91db70e8-4c3e2778-3686400-17be726848e907%22%7D',
        'sajssdk_2015_cross_new_user': '1',
        'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6Ik9xYjJxeE54YVU5SWdQRDJaOVJwMGc9PSIsInZhbHVlIjoiclwvVERqWUJtNGV0cWgxbVhDdnRTSlAyMkxJVjFKaUFQWDd6QW5YVElNWko2MUc3OWdEVnNyd3ZLXC9RTk9GYVJqekdjaHM1Wjk0WHZLM3RuZXBCTjdUOGk5WVlIMlVjWms3dkxzVWdWYjRnOD0iLCJtYWMiOiI3YTM0YzFjMTRhYzhiNDM2ODQ3MTVmYzg1YThkNjNjNDg1OTM5YzhhYTI0MWM3MzI2MTJjNTIzYjdlMDE4YTg0In0%3D',
        'user_id': '411771879',
        'ACCOUNT_LOGGED_USER_FROM_WWW': 'LtV6IRGzD2JF5FkllpaCuA%3D%3D',
        'CONSOLES_TOKEN_FROM_WWW': 'RNkPDhex7h05LlVyMvyB0g%3D%3D',
        'acw_tc': '2760827616317040752267001ee14cd9cbf9806813538eb10f3d3f33e5af12',
        '_gat': '1',
    }



    proxies = {
        # searched from Internet
        "http":"211.65.197.93:80",
    }



    headers = {
        'User-Agent':"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Referer': 'https://www.taptap.com/topic/19232532',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'TE': 'trailers',
    }

    fileUser = open("userlist"+str(beginNo)+"-"+str(endNo) + ".txt", 'w', encoding='utf-8')
    fileReview = open("review"+str(beginNo)+"-"+str(endNo) + ".txt", 'w', encoding='utf-8')
    filePost = open("post"+str(beginNo)+"-"+str(endNo) + ".txt", "w", encoding='utf-8')
    fileApp = open("app"+str(beginNo)+"-"+str(endNo) + ".txt",'w', encoding='utf-8')

    userlist = []
    applist = []

    filetop150 = open("top150HotApp.txt",'r', encoding='utf-8')
    line = filetop150.readline()
    while line:
        applist.append(int(line))
        line = filetop150.readline()
    filetop150.close()

# read app from beginNo to endNo
    for i in range(beginNo, endNo):
        # 调用方法
        getAppData(appId= int(applist[i]),fileApp=fileApp)
        getReviewData(appId=int(applist[i]),fileReview=fileReview,userList=userlist)
        getPostData(appId=int(applist[i]),filePost=filePost,userList=userlist)

# put all users in userlist into fileuser
    for i in range(0,len(userlist)):
        fileUser.write(str(userlist[i]) + '\n' )

    fileReview.close()
    fileApp.close()
    fileUser.close()
    filePost.close()




