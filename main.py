import re
import sys
from urllib.parse import quote_plus
import praw
import configparser

import requests

config = configparser.ConfigParser()
try:
    config.read('config.ini')
except configparser.Error as e:
    print(f"Error reading config.ini: {e}")
    sys.exit(1)


def load_config(user_section):
    try:
        return (
            config.get(user_section, 'client_id').replace('"', ''),
            config.get(user_section, 'client_secret').replace('"', ''),
            config.get(user_section, 'username').replace('"', ''),
            config.get(user_section, 'password').replace('"', ''),
            config.get(user_section, 'user_agent').replace('"', ''),
        )
    except configparser.Error as e:
        raise ValueError(f"Error loading credentials for {user_section} from config.ini: {e}")

api_key = config.get('zoya', 'api_key').replace('"', ''),
api_url = config.get('zoya', 'api_url').replace('"', ''),
client_id, client_secret, username, password, user_agent = load_config("bot1")



reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

def get_halal_status(item_name):
    url = api_url[0]
  
    body = """ 
            query BasicCompliance {
                basicCompliance {
                    report(symbol: "%s") {
                        status
                        name
                        reportDate
                    }
                }
            }
    """ % item_name
    
    response = requests.post(url=url, json={"query": body}, headers={"Authorization": api_key[0]}) 
    print("response status code: ", response.status_code) 
    if response.status_code == 200: 
        print("response : ", response.content) 

def process_submission(submission):
    # Ignore titles with more than 10 words as they probably are not simple questions.
    if len(submission.title.split()) > 10:
        return

    normalized_title = submission.title.lower()
    print(normalized_title)
    try:
        # Extract the text between the last word and "Halal".
        halalItemName = re.search(r'^.*[^\.*](.*?) halal', normalized_title).group(1)
        api_result = get_halal_status(halalItemName)
        url_title = quote_plus(submission.title)
        reply_text = REPLY_TEMPLATE.format(halalItemName)
        print(f"Replying to: {submission.title}")
        submission.reply(reply_text)
    except Exception as e:
        print(f"Error processing submission: {e}")
        pass



print(reddit.user.me())


REPLY_TEMPLATE = "Test reply to: {0}"

# array of subreddits to monitor
subreddits_list = ['testingground4bots']

subreddit = reddit.subreddit('testingground4bots')

for submission in subreddit.stream.submissions():
     process_submission(submission)



#comments = subreddit.stream.comments()

#for comment in comments: 
#    text = comment.body ## Get comment's body
#    author = comment.author ## Get comment's body
#    if 'testeriwtndsnf' in text.lower():
#        ## Generate message
#        message = "Hey u/{0}, it looks".format(author)
#        comment.reply(message) ## Send message