from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array

INPUT_SIZE = (224, 224)


def image_data(image_path):
    im = img_to_array(load_img(image_path, color_mode="rgb", target_size=INPUT_SIZE))
    shape = (1,) + im.shape
    return preprocess_input(im.reshape(shape))


def predict(model, im_data):
    prediction = model.predict(im_data)
    labels = decode_predictions(prediction)
    return [(label[1], label[2]) for label in labels[0]]



