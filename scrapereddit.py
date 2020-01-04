import praw
from prawcore.exceptions import NotFound, BadRequest
import yagmail
import os

# Insert subreddits you want to get news from
# eg. ['learnprogramming', 'python']

SUBREDDITS = []

# Set email and password as environment variables
email = os.environ.get('GmailAccount')
password = os.environ.get('GmailPass')




reddit = praw.Reddit(
    client_id='',       # Client id here
    client_secret='',   # client secret
    user_agent='Myapp'  # Put anything here
)



def get_hot_posts(subreddit, posts_limit=5):  # gets 5 ( or posts_limit) hot posts from a subreddit
    subreddit = reddit.subreddit(subreddit)
    hot_posts = []
    try:
        for submission in subreddit.hot(limit=posts_limit):
            if submission.stickied == False:
                post = {
                'title': submission.title,
                'score': submission.score,
                'url': submission.shortlink ,
                'author': submission.author.name,
                'id': submission.id,
                'subreddit': submission.subreddit.display_name
                }
                hot_posts.append(post)

    except (NotFound, BadRequest, UnboundLocalError) as e:
        print(e)
    else:
        return hot_posts



def get_top_post(subbreddit):   # Returns the post with the highest score from a single subreddit
    posts = get_hot_posts(subbreddit)
    scores = []
    for post in posts:
        scores.append(post['score'])
        topscore = max(scores)
        return [post for post in posts if post['score'] == topscore]


def get_all_top_posts(subreddits=SUBREDDITS):  # Gets the top post with highest score from every subreddit
    posts = []
    for subreddit in subreddits:
        top_post = get_top_post(subreddit)
        posts.append(top_post[0])   # Index 0: to get rid of list
    return posts




def email_message(posts):
    messages = []
    for post in posts:
        messages.append(f"({post['score']}) - <a href='{post['url']}'>{post['title']}</a> in <b>r/{post['subreddit']}</b>\n") # Message format
    return ''.join(messages)

def send_email(message):
    yag = yagmail.SMTP(email)
    yag.send(
    to=email,
    subject='Reddit digest',
    contents=f'''
    {message}'''
    )

def main():
    posts = get_all_top_posts(SUBREDDITS)

    message = email_message(posts)
    send_email(message)
    print('Email sent!')

if __name__ == '__main__':
    try:
        main()
    except TypeError:
        print("One of the subreddits you provided doesn't exist.")
