from atproto import Client
import argparse

client = Client()

parser = argparse.ArgumentParser()
parser.add_argument('email', nargs='?', type=str, help='Account email')
parser.add_argument('password', nargs='?', type=str, help='Account password')
parser.add_argument('-s', type=str, help='Write session token to file')
parser.add_argument('-t', type=str, help='File with session token')
args = parser.parse_args()

if args.t:
    print('Logging in with session token')
    with open(args.t) as f:
        session_string = f.read()
    
    client.login(session_string=session_string)
else:
    print('Logging in')
    client.login(args.email, args.password)

if args.s:
    session_string = client.export_session_string()
    with open(args.s, 'w') as f:
        f.write(session_string)

if client.me.posts_count == 0:
    print('No posts to delete')
    exit(1)

cursor = None

# go until you find a post, not a repost
while True:
    posts = client.get_author_feed(client.me.did, cursor=cursor, limit=100)
    cursor = posts.cursor

    for feed_view in posts.feed:
        if feed_view.post.author.handle == client.me.handle:
                client.delete_post(feed_view.post.uri)
                print('Deleted last post')
                exit(1)
