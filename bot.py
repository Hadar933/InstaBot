import random, shutil, os
from instabot import Bot
from instapy import InstaPy, smart_run

from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions, VGG16
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# TODO: set username and password
MY_USERNAME = ""
MY_PASSWORD = ""

EMOJIES = ["🥰", "🤑", "🏠", "🏘️", "🥳", "💙", "🙌", "🌲", "🌴", "🏛", "🏘", "🏡"]

HASHTAGS = "#homeinteriors #luxuryliving #luxurioushome #gardendesign" \
           " #homeinspiration #interiordesigners #interiordecoration #interiorandhome" \
           " #gardendecor #designinterior #interiordesigngoals #interiordesignlovers #interiordesigntrends"

USERNAMES = ["archdigest", "homeadore", "beautifulhotels", "archidesiign", "design_interior_homes", "mymodern.interior",
             "japandi.interior", "article", "jossandmain", "serenaandlily"]

COMMENTS = ['Nice shot! @{}', 'I love your profile! @{}', 'Your feed is an inspiration :thumbsup:',
            'Just incredible :open_mouth:', 'Love your posts @{}', 'Looks awesome @{}', ':raised_hands: Yes!',
            'Loving it @{} :muscle:']


def get_image_description(image_path):
    """
    uses VGG16 neural-network to get image description.
    the description will be used to generate more suited comments.
    :param image_path: media item to get description of
    :return: image description (string)
    """
    im_array = img_to_array(load_img(image_path, color_mode="rgb", target_size=(224, 224)))
    shape = (1,) + im_array.shape
    image_data = preprocess_input(im_array.reshape(shape))
    prediction = VGG16().predict(image_data)
    labels = decode_predictions(prediction)
    labels = [(label[1], label[2]) for label in labels[0]]
    print("description confident=",labels[0][1])
    return (labels[0][0]).replace("_", " ")


def download_media(username, maximum, media_type):
    """
    downloads media from username using instagram-scraper module (via cmd command)
    :param username: your username
    :param media_type: video,story,image (more than 1 : story-image for ex)
    :param maximum: maximum items to get
    """
    command = f"instagram-scraper {username} -u {MY_USERNAME} -p {MY_PASSWORD} --maximum {maximum}" \
              f" --media-types {media_type} --media-metadata --profile-metadata"
    os.system('cmd /c' + command)


def clean_up(dir_name):
    """
    removes dir_name if it exists
    :param dir_name: if dir_name = config - insta-bot must be used without
                    a config Directory initialized (it will initialize one itself).
                    otherwise (dir_name != config) its regular deletion
    """
    if os.path.exists(dir_name):
        print(f"deleting {dir_name} directory...")
        shutil.rmtree(dir_name)


def set_image_caption(media_name):
    """
    generates an informative image caption
    :return: an informative image caption
    """
    desc = get_image_description(media_name)
    pre_set_text = [f'What do you think of this {desc}?', f'This {desc} is amazing!',
                    f'Comment your thoughts on this {desc}', f'this {desc} is Beautiful!',
                    f'Tag someone who will like this {desc}']
    creator_credit = media_name.split("/")[0]
    main_text = random.choice(pre_set_text) + " " + random.choice(EMOJIES)
    entire_block = f"{main_text}\n" \
                   f"🙋🏼‍♀ Follow: @{MY_USERNAME}\n" \
                   f"📣 Credit: @{creator_credit}\n" \
                   f".\n" \
                   f".\n" \
                   f".\n" \
                   f"{HASHTAGS}"
    return entire_block


def upload_media(media_name):
    """
    a helper method that uses insta-bot module to upload media to instagram account
    :param media_name: media location to upload
    """
    bot = Bot()
    bot.login(username=MY_USERNAME, password=MY_PASSWORD)
    caption = set_image_caption(media_name)
    print(f"uploading {media_name}")
    bot.upload_photo(media_name, caption)


def download_upload_media(username, amount, media_type):
    """
    uploads media to instagram account
    :param username: your username
    :param amount: number of media items to upload
    :param media_type: video/image/etc...
    """
    download_media(username, amount, media_type)
    clean_up("config")
    file_names = os.listdir(username)
    media_to_upload = [item for item in file_names if item.endswith(".jpg")][1]  # without profile pic
    upload_media(username + "/" + media_to_upload)
    clean_up(username)


def engage():
    """
    uses insta-py to like and follow users
    """
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


def daily_task(iterations, num_media_items, media_type):
    """
    :param media_type: media type to upload
    :param num_media_items: number of media items to upload
    :param iterations: set engage loop iterations
    1. downloads content
    2. uploads content to instagram
    3. set likes and follows
    """
    todays_username = random.choice(USERNAMES)
    download_upload_media(todays_username, num_media_items, media_type)
    for i in range(iterations):
        engage()


if __name__ == '__main__':
    # daily_task(5, 3, 'image')
    print(set_image_caption("Capture.JPG"))
