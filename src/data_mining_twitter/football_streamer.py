import twitter
import csv
import re
import time

access_token = "3340873871-WcyL5tEeNFLWNsSfp7rX0YcOlNF77eqwSJuEq33"
access_token_secret = "KWBNhNbjqyNEraZ2XKlkWnNFs8Ms8DxNsRWup1tToAEME"
consumer_key = "no8HD5djfkaHyjfdO1ajoWPym"
consumer_secret = "S4rgAV5LEh0BVRVA0GWrqZZ3TThYFquFHfpk2eKUPoQVgtKzQJ"


def tweets_analyzer(text):
    intersection = set(text.split()) & set(football_clubs)
    patterns = ['\d+ *\- *\d+']
    reg_result = []
    for pattern in patterns:
        reg_result += re.findall(pattern, text)

    if (len(intersection) == 2) and reg_result:
        intersection = list(intersection)
        intersection = '{};{};{}'.format(intersection[0], intersection[1], reg_result)
        return intersection

    return False


def extract_link(text):
        regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        match = re.search(regex, text)
        if match:
            return match.group()
        return ''

api = twitter.Api(consumer_key=consumer_key,consumer_secret=consumer_secret,
                  access_token_key=access_token, access_token_secret=access_token_secret)

football_clubs = []
with open('football_clubs.csv', 'rb') as f:
    clubs = csv.reader(f)
    for club in clubs:
        football_clubs.append(club[0])

channels_id = []
with open('accounts.csv', 'rb') as f:
    accounts = csv.reader(f)
    for account in accounts:
        channels_id.append(account[0].split(';')[0])

print 'user_id;tweets_id;date;text;link'
for user in channels_id:
    tweets_count = 0
    last_id = None

    while tweets_count < 5000:
        try:
            statuses = api.GetUserTimeline(user_id=user, count=200, max_id=last_id)
            for s in statuses:
                if last_id == s.id:
                    continue
                last_id = s.id
                if s.text:
                    intersection_result = tweets_analyzer(s.text.encode('utf-8'))
                    if intersection_result:
                        row = '{user_id};{tweets_id};{date};{text};{link}'\
                            .format(user_id=user, tweets_id=s.id, date=s.created_at.encode('utf-8'),
                                    text=intersection_result, link=extract_link(s.text.encode('utf-8')))
                        print row
            tweets_count += 200
        except twitter.TwitterError:
            print '********* sleep 5 min *********'
            time.sleep(5*60)
            continue

print "Done!"
