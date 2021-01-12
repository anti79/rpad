import praw
import datetime
import time
import aid_api
from aid_api import AID
from pbwrap import Pastebin
reddit = praw.Reddit("rpad",
                     user_agent="/u/rpadbot user agent")
pastebin = Pastebin("l7ibOPG3CktmIkrxLfNsDwHNqmE7AvML") #for adventure memory, currently not used
def getRawPaste(link):
    link = link.replace("https://pastebin.com/", "https://pastebin.com/raw/")
    return link
subreddit = reddit.subreddit("redditplaysaidungeon")
while True:
    for submission in (subreddit.new(limit=1)): #get last post
        newest = submission
    submission_comments = newest.comments
    real_comments = [comment for comment in submission_comments if isinstance(comment, praw.models.Comment) and not isinstance(comment.parent(), praw.models.Comment) and not comment.body[0]=='\\' and comment.author.name!="AutoModerator"] #remove child comments
    real_comments.sort(key=lambda comment: comment.score, reverse=True)
    if(len(real_comments)>0): 
        top_comment = real_comments[0].body
        top_comment = top_comment[0:4000]
        print("Found top comment!")
        print(top_comment)
        if(top_comment!="!wait"): AID.sendAction(top_comment, "do")
        else: AID.sendAction("", "do")
        print("Sent action!")
        try:
            real_comments[0].reply("Congrats, your action was the top comment! Now try sorting the sub by new, the AI should respond to it shortly.")
        except:
            print("Reddit ratelimit, waiting for 15 min")
            time.sleep(900)
            real_comments[0].reply("Congrats, your action was the top comment! Now try sorting the sub by new, the AI should respond to it shortly.")
        print("Replied to top comment!")
##########COMPOSING THE POST#############
        ai_response = AID.getAIResponse()
        print("Got the AI response!")
        print(ai_response)
        post = ""
        #post = ai_response + "\n\n" + "\__________________________"+  "\n\n" + "^(Current quests:) "
        post = ai_response
        #quests = AID.getQuests()
        #if(len(quests)==0): post += "^(none)\n"
        #else: 
        #    for quest in quests:
        #        quest = "^(" + quest + ")" + "\n"
        #        post += quest
        #post += "^([AI Memory](" + getRawPaste(pastebin.create_paste("Memory: " + AID.getMemory())) + "))"
        postTitle = "You " + top_comment[0].lower() + top_comment[1:len(top_comment)] #make the first letter lowercase
########################################
        try:
            subreddit.submit(title=postTitle, selftext=post) 
        except:
            print("Reddit ratelimit, waiting for 15 min")
            time.sleep(900)
            subreddit.submit(title=postTitle[0:299], selftext=post)
        print("New post submitted.")
        print("Now sleeping for an hour...")
        print("Current time: " + str(datetime.datetime.now().time()))
        time.sleep(3600)
    print("Still no comments... waiting")
    time.sleep(10)

        