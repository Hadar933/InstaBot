import random
import shutil
from instabot import Bot
import os
from instapy import InstaPy, smart_run


MY_USERNAME = "homeinteriorfreak"
MY_PASSWORD = "79518463"

EMOJIES = ["🥰", "🤑", "🏠", "🏘️", "🥳", "💙", "🙌", "🌲", "🌴", "🏛", "🏘", "🏡"]

PREFIX = ["What do you think?", "Follow for more!", "Comment your thoughts", "Get inspired here!",
          "This one is BEAUTIFUL!"]

HASHTAGS = "#homeinteriors #luxuryliving #luxurioushome #gardendesign" \
           " #homeinspiration #interiordesigners #interiordecoration #interiorandhome" \
           " #gardendecor #designinterior #interiordesigngoals #interiordesignlovers #interiordesigntrends"

USERNAMES = ["archdigest", "homeadore", "beautifulhotels", "archidesiign", "design_interior_homes", "mymodern.interior",
             "japandi.interior", "article", "jossandmain", "serenaandlily"]

COMMENTS = ['Nice shot! @{}', 'I love your profile! @{}', 'Your feed is an inspiration :thumbsup:',
            'Just incredible :open_mouth:', 'Love your posts @{}', 'Looks awesome @{}', ':raised_hands: Yes!',
            'Loving it @{} :muscle:']


def download_media(username, maximum, media_type):
    """
    dowmloads media from some ig_users.txt
    :param media_type: video,story,image (more than 1 : story-image for ex)
    :param maximum: maximum items to get
    """
    command = f"instagram-scraper {username} -u {MY_USERNAME} -p {MY_PASSWORD} --maximum {maximum}" \
              f" --media-types {media_type} --media-metadata --profile-metadata"
    os.system('cmd /c' + command)


def clean_up(dir_name):
    """
    :param dir_name: if dir_name = config - insta-bot must be used without
                    a config Directory initialized (it will initialize one itself).
                    otherwise (dir_name != config) its regular deletion
    """
    if os.path.exists(dir_name):
        print(f"deleting {dir_name} directory...")
        shutil.rmtree(dir_name)


def upload_media_helper(filename):
    bot = Bot()
    bot.login(username=MY_USERNAME, password=MY_PASSWORD)
    credit = filename.split("/")[0]
    first_line = random.choice(PREFIX) + ' ' + random.choice(EMOJIES)
    caption = f"{first_line}\n" \
              f"📣 Credit: @{credit}\n \
               🙋🏼‍♀ Follow @homeinteriorfreak" \
              f".\n" \
              f".\n" \
              f".\n" \
              f"{HASHTAGS}"
    print(f"uploading {filename}")
    bot.upload_photo(filename, caption)


def upload_media(username, amount, media_type):
    download_media(username, amount, media_type)
    clean_up("config")
    file_names = os.listdir(username)
    media_to_upload = [item for item in file_names if item.endswith(".jpg")][1]  # without profile pic
    upload_media_helper(username + "/" + media_to_upload)
    clean_up(username)


def engage():
    session = InstaPy(username=MY_USERNAME,
                      password=MY_PASSWORD,
                      headless_browser=True)
    with smart_run(session):
        session.set_relationship_bounds(enabled=True, delimit_by_numbers=True, max_followers=5000)
        session.set_do_follow(True, percentage=80)
        session.set_user_interact(amount=3, randomize=True, percentage=100, media='Photo')
        # session.set_do_comment(enabled=True, percentage=50)
        # session.set_comments(COMMENTS)

        two_random_hashtags = [item[1:] for item in random.choices(HASHTAGS.split(" "), k=5)]
        session.like_by_tags(two_random_hashtags, amount=100)


def daily_task():
    todays_username = random.choice(USERNAMES)
    todays_amount = 2
    upload_media(todays_username, todays_amount, 'image')
    engage()


if __name__ == '__main__':
    upload_media(random.choice(USERNAMES), 2, 'image')
    for i in range(5):
        engage()
