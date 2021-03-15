#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3


import config
import tweepy
import re
import argparse


# Enviromental variables and flags
tweepy_consumer_key = config.TWEEPY_CONSUMER_KEY
tweepy_consumer_secret = config.TWEEPY_CONSUMER_SECRET
tweepy_access_token_secret = config.TWEEPY_ACCESS_TOKEN_SECRET
tweepy_access_token = config.TWEEPY_ACCESS_TOKEN
tweepy_callback_uri = 'oob'
auth = tweepy.OAuthHandler(
    tweepy_consumer_key, tweepy_consumer_secret, tweepy_callback_uri)
auth.set_access_token(tweepy_access_token, tweepy_access_token_secret)
api = tweepy.API(auth)


# Define flags
parser = argparse.ArgumentParser()
parser.add_argument(
    "--numbers-only", help="Print only numbers of deaths and infections, ommiting date", action="store_true")
parser.add_argument("--range", type=int, help="Set range for tweet scanning")

args = parser.parse_args()


scan_range = 0

if args.range:
    scan_range = args.range
else:
    scan_range = int(input('How many tweets do you want to scan? '))

#  Get deaths from twitter


def get_deaths():
    death_dict = {}
    for tweet in tweepy.Cursor(api.user_timeline, id='MZ_GOV_PL').items(scan_range):
        content = tweet.text
        posted_at = str(tweet.created_at)
        date_formatted = posted_at.split(' ', 1)[0]
        if "natomiast z powodu współistnienia" in content:
            numbers = re.findall(r'\d+', content)
            death_sum = int(numbers[1]) + int(numbers[3])
            death_dict[date_formatted] = death_sum
    return death_dict

#  Get infections from twitter


def get_infections():
    formatted_infection_numbers_dict = {}
    for tweet in tweepy.Cursor(api.user_timeline, id='MZ_GOV_PL').items(scan_range):
        content = tweet.text
        posted_at = str(tweet.created_at)
        date_formatted = posted_at.split(' ', 1)[0]
        if "Mamy" in content and "województw" in content:
            initial_numbers = re.sub(r'(\d)\s+(\d)', r'\1\2', content)
            formatted_infection_numbers = re.findall(
                r'\d+', initial_numbers)[0]
            formatted_infection_numbers_dict[date_formatted] = formatted_infection_numbers
    return formatted_infection_numbers_dict


def print_results():
    deaths = get_deaths()
    infections = get_infections()
    print("Deaths:")
    for k_d, v_d in reversed(deaths.items()):
        print(k_d, ' ', v_d, ' deaths')
    print("Infections:")
    for k_i, v_i in reversed(infections.items()):
        print(k_i, ' ', v_i, ' infections')


def print_results_numbers():
    deaths = get_deaths()
    infections = get_infections()
    print("Deaths:")
    for k_d, v_d in reversed(deaths.items()):
        print(v_d)
    print("Infections:")
    for k_i, v_i in reversed(infections.items()):
        print(v_i)


if args.numbers_only:
    print_results_numbers()
else:
    print_results()
