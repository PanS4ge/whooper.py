import os

def clean_cmd():
    if (os.name != "nt"):
        os.system("clear")
    else:
        os.system("cls")

try:
    from PIL import Image
    import cv2
    import glob
    import time
    import requests
    import math
    import json
except ImportError:
    os.system("pip install Pillow opencv-python requests --user")
    clean_cmd()
    print("Finished downloading packages, reset script")
    input("Press enter to continue")
    exit()


ascii_characters_by_surface = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
whopper_ad = [
    "Whopper, Whopper, Whopper, Whopper,",
    "Junior, double, triple Whopper,",
    "Flame-grilled taste with perfect toppers,",
    "I rule this day.",
    "",
    "Lettuce, mayo, pickle, ketchup,",
    "It's OK if I don't want that,",
    "Impossible or bacon Whopper,",
    "Any Whopper my way.",
    "",
    "You rule, you're seizing the day,",
    "At BK, have it your way.",
    "",
    "You rule!",
    "_______________",
    "Initializing..."
]

brighten = ""
frames = ""
width = ""
height = ""
max_brightness = ""
debug = ""
nocolor = ""

def download_whooper():
    if not(os.path.exists(f"{os.getcwd()}/WHOOPER.mp4")):
        a = requests.get("http://pansage.pl/WHOOPER.mp4")
        with open("WHOOPER.mp4", "wb") as WHOP:
            WHOP.write(a.content)

def cbool(b : str):
    if(b.lower() == "false"):
        return False
    elif(b.lower() == "true"):
        return True
    else:
        configs(True)
        print("Called reinit of config")
        input()
        exit()
        return False

def configs(force):
    global brighten, frames, width, height, max_brightness, debug, nocolor
    if not (os.path.exists(f"{os.getcwd()}/config.json")) or force:
        a = json.loads("{}")
        a['brighten'] = 1.5
        a['frames'] = 23.976024
        a['width'] = 98
        a['height'] = -1
        a['height_note'] = "-1 = use aspect ratio"
        a['max_brightness'] = 255 * 3
        a['debug'] = str(False)
        a['nocolor'] = str(False)
        brighten = float(a['brighten'])
        frames = float(a['frames'])
        width = int(a['width'])
        height = int(a['height'])
        max_brightness = int(a['max_brightness'])
        debug = cbool(a['debug'])
        nocolor = cbool(a['nocolor'])
        with open(f"{os.getcwd()}/config.json", "w") as conf:
            conf.write(json.dumps(a, indent=4))
    else:
        try:
            with open(f"{os.getcwd()}/config.json", "r") as conf:
                a = json.loads(conf.read())
                brighten = float(a['brighten'])
                frames = float(a['frames'])
                width = int(a['width'])
                height = int(a['height'])
                max_brightness = int(a['max_brightness'])
                debug = cbool(a['debug'])
                nocolor = cbool(a['nocolor'])
        except TypeError as te:
            print(str(te) + " - Initiated CONFIG reset")
            configs(True)

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[39m".format(r, g, b, text)


def brighten_color(color):
    global nocolor
    if(nocolor):
        return 0
    col = math.ceil(color * brighten)
    if (col >= 255):
        return 255
    else:
        return color


def convert_pixel_to_character(pixel):
    (r, g, b) = pixel
    pixel_brightness = r + g + b
    try:
        brightness_weight = len(ascii_characters_by_surface) / max_brightness
    except TypeError:
        configs(True)
        clean_cmd()
        print("Initiated restart of configs")
        input("Press enter to exit")
        return
    index = int(pixel_brightness * brightness_weight) - 1
    return colored(brighten_color(r), brighten_color(g), brighten_color(b), ascii_characters_by_surface[index])


def convert_to_ascii_art(image):
    global brighten, frames, width, height, max_brightness, debug, nocolor
    width_x, height_x = image.size
    aspect_ratio = height_x / width_x
    new_width = width
    new_height = 0
    if (height == -1):
        new_height = int(aspect_ratio * new_width * 0.5)
    else:
        new_height = height
    if(type(new_width) == type("test string")):
        configs(True)
        clean_cmd()
        print("Initiated restart of configs")
        input("Press enter to exit")
        return
    if(type(new_height) == type("test string")):
        configs(True)
        clean_cmd()
        print("Initiated restart of configs")
        input("Press enter to exit")
        return
    image.resize((new_width, new_height))
    ascii_art = []
    for y in range(0, height_x - 1, math.floor(height_x / new_height)):
        line = ''
        for x in range(0, width_x - 1, math.floor(width_x / new_width)):
            px = image.getpixel((x, y))
            line += convert_pixel_to_character(px)
        ascii_art.append(line)
    return ascii_art


def asciify_image(image_t):
    global brighten, frames, width, height, max_brightness, debug
    image = Image.open(image_t)
    ascii_art = convert_to_ascii_art(image)
    if(debug):
        print("Frame " + str(glob.glob(f"{os.getcwd()}/frm/*.jpg").index(image_t) + 1) + "/722")
        print("Size: " + str(len(ascii_art[0])) + "x" + str(len(ascii_art)))
        print("-------------------------------------------------------------------------------")
    else:
        save_as_text(ascii_art)
    time.sleep(1 / frames)
    if not (debug):
        clean_cmd()


def save_as_text(ascii_art):
    for line in ascii_art:
        print(line)


def frameify():
    try:
        os.mkdir("frm")
    except OSError:
        pass
    if (len(glob.glob(f"{os.getcwd()}/frm/*.jpg")) != 722):
        # Load the video file
        video = cv2.VideoCapture("WHOOPER.mp4")

        # Loop through the video frames and extract them
        success, image = video.read()
        count = 0
        while success:
            # Write the frame to a file
            cv2.imwrite(f"{os.getcwd()}/frm/frame{count}.jpg", image)

            # Read the next frame
            success, image = video.read()
            count += 1

        # Release the video
        video.release()


def init():
    configs(False)
    clean_cmd()
    for x in whopper_ad:
        print(x)
    download_whooper()
    frameify()
    clean_cmd()
    for x in glob.glob(f"{os.getcwd()}/frm/*.jpg"):
        try:
            if (asciify_image(x) != None):
                print(asciify_image(x))
        except:
            print(asciify_image(x))


if (__name__ == "__main__"):
    init()
