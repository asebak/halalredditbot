import sys
import praw
import configparser

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

client_id, client_secret, username, password, user_agent = load_config("bot1")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)


print(reddit.user.me())


# array of subreddits to monitor
subreddits_list = ['testingground4bots']

subreddit = reddit.subreddit('testingground4bots')

## This maintains a constant stream of comments in real time
comments = subreddit.stream.comments()

## Looks at every 
for comment in comments: 
    text = comment.body ## Get comment's body
    author = comment.author ## Get comment's body
    if 'testeriwtndsnf' in text.lower():
        ## Generate message
        message = "Hey u/{0}, it looks".format(author)
        comment.reply(message) ## Send message