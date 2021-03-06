import sys
from flask import Flask, render_template
from tweetie import *
from colour import Color
from numpy import argsort, median


reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)


def add_color(tweets):
    """
    Given a list of tweets, one dictionary per tweet, this function will add
    a "color" key to each tweets dictionary with a value
    containing a color graded from red to green. Pure red
    would be for -1.0 sentiment score and pure green would be for
    sentiment score 1.0.

    Output:

    -1 should get mapped to 0
    1 should get mapped to 100
    0 should get mapped to 50
    0.5 should get mapped to 75
    -0.5 should get mapped to 25
    
    """
    colors = list(Color("red").range_to(Color("green"), 100))
    for t in tweets:
        score = t['score']
        if score > 0:
            score = int(round(score * 50 + 50))
        elif score < 0:
            score = int(round(score * 50 + 50))
        elif score ==0:
            # print score
            score = int(score) + 50

        t['color'] = colors[score]


@app.route("/<name>")


def tweets(name):
    "Display the tweets for a screen name color-coded by sentiment score"
    user = api.get_user(name)  
    usersn = user.screen_name

    fetch = fetch_tweets(api, name)
    tweets = fetch['tweets']
    add_color(tweets)

    test1 = [fetch['tweets'][i]['text'] for i in range(len(fetch['tweets']))]
    score1 = [fetch['tweets'][i]['score'] for i in range(len(fetch['tweets']))]
    medianscore = round(median(score1),5)
    score1 = [round(score, 4) for score in score1]
    col = [fetch['tweets'][i]['color'] for i in range(len(fetch['tweets']))]
    tweetList = []
    for status in tweepy.Cursor(api.user_timeline, id = name).items(100):
      tweetList.append(status)
    tweetid = ["https://twitter.com/statuses/" + str(fetch['tweets'][i]['id']) for i in range(len(fetch['tweets']))]
    
    ziptweetscore = zip(test1,score1, col, tweetid)
    return render_template('tweets.html', test1 = ziptweetscore, test = usersn, test2 = medianscore)

@app.route("/following/<name>")


def following(name):
    """
    Display the list of users followed by a screen name, sorted in
    reverse order by the number of followers of those users.
    """
    
    user = api.get_user(name)  
    usersn = user.screen_name
    fetch = fetch_following(api, name)
    
    numfollower = [fetch[i]['followers'] for i in range(len(fetch))]
    sortorder = argsort(numfollower)

    numfollower = [numfollower[i] for i in sortorder[::-1]]
    fullname = [fetch[i]['name'] for i in sortorder[::-1]]
    createdate = [fetch[i]['created'] for i in sortorder[::-1]]
    picture = [fetch[i]['image'] for i in sortorder[::-1]]
    screenname = ['https://twitter.com/' + fetch[i]['screen_name'] for i in sortorder[::-1]]
    ziptweet = zip(fullname, numfollower, createdate, picture, screenname)
    return render_template('following.html', test1 = ziptweet, test = usersn)
    
# i = sys.argv.index('server:app')
twitter_auth_filename = sys.argv[1]
api = authenticate(twitter_auth_filename)
app.run('localhost')