#!/usr/bin/env python3
import argparse
import requests


def get_info_from_api(method_name, **parameters):
    url = "https://api.vk.com/method/{}?".format(method_name)
    for key, val in parameters.items():
        url += "{}={}&".format(key, val)
    url = url[:-1]
    r = requests.get(url)
    return r.json().get('response', [])


argparser = argparse.ArgumentParser(description="vk find")
argparser.add_argument("id", help="Initial user id")
argparser.add_argument("token", help="Access token")
argparser.add_argument("--num", help="Number of results", default=20)
args = argparser.parse_args()

with open('keywords.txt') as f:
    keywords = [word.strip() for word in f.read().split(',')]

users = [args.id]
checked = []
ads = []
while len(ads) < args.num:
    for user in users[:]:
        users += list(filter(lambda user: user not in checked,
                      get_info_from_api('friends.get', user_id=user,
                                        access_token=args.token)))

        for post in get_info_from_api('wall.get', owner_id=user,
                                      count=15, access_token=args.token):
            if type(post) != dict:
                continue
            text = post.get('text', '')
            if len(text) > 3000 or text in ads:  # rental ads are not so long
                continue
            for keyword in keywords:
                if keyword in text:
                    ads.append(text)
                    with open('result', 'a') as result:
                        result.write('http://vk.com/wall{}_{}\n'.format(
                            post['from_id'], post['id']))
                        result.write(text + "\n\n--------------------------\n")
                    break
