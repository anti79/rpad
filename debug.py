import praw
import datetime
import time
import aid_api
from aid_api import AID
from pbwrap import Pastebin
reddit = praw.Reddit("rpad",
                     user_agent="/u/rpadbot user agent")
pastebin = Pastebin("l7ibOPG3CktmIkrxLfNsDwHNqmE7AvML") #for adventure memory
def getRawPaste(link):
    link = link.replace("https://pastebin.com/", "https://pastebin.com/raw/")
    return link
subreddit = reddit.subreddit("subforbots")
for submission in (subreddit.new(limit=1)): #get last post
    newest = submission
submission_comments = newest.comments
real_comments = [comment for comment in submission_comments if isinstance(comment, praw.models.Comment) and not isinstance(comment.parent(), praw.models.Comment) and not comment.body[0]=='\\' and not comment.author.name=="automoderator"] #remove child comments
real_comments.sort(key=lambda comment: comment.score, reverse=True)
print(real_comments[0].author.name)