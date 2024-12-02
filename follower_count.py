from atproto import Client
import argparse

client = Client()

parser = argparse.ArgumentParser()
parser.add_argument('email', nargs='?', type=str, help='Account email')
parser.add_argument('password', nargs='?', type=str, help='Account password')
parser.add_argument('handle', type=str, help='Handle')
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

print(client.get_profile(args.handle).followers_count)
