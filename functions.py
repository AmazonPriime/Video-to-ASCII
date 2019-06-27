import numpy as np
import text_image as ti
import cv2, os, PIL, multiprocessing
import PIL.Image, PIL.ImageFont, PIL.ImageOps, PIL.ImageDraw
from PIL import Image

greyscale = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def cleanFolders():
    folders = ['data', 'images', 'imagesOut', 'imagesOutPng']
    for folder in folders:
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
    print("Cleaned the folders, emptied 'data', 'images', 'imagesOut' and 'imagesOutPng'.")

def getVideoArray(filename):
    cap = cv2.VideoCapture('input/{}'.format(filename))
    frameCount, frameWidth, frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vidArray = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
    fc, ret = 0, True
    while True:
        d = cap.read()
        if d == (False, None):
            break;
        ret, vidArray[fc] = d
        fc += 1
    cap.release()
    np.save("data/array.npy", vidArray)
    print("Created Numpy array and stored in data/array.npy")

def getAscii():
    max = len(os.listdir("images"))
    pool = multiprocessing.Pool(processes = 4)
    pool.map(imageToAscii, (("images/{}.jpg".format(i), "imagesOut/{}.txt".format(i), 250, 0.43) for i in range(max)))
    print("Converted the images into ASCII text files and stored files in imagesOut/<num>.txt")

def convertImages():
    max = len(os.listdir("images"))
    pool = multiprocessing.Pool(processes = 4)
    pool.map(ti.main, (i for i in range(max)))
    print("Converted the ASCII text files to images and stored them in imagesOutPng/<num>.png")

def getImages(filename):
    data = np.load("data/{}".format(filename))
    for i,d in enumerate(data):
        cv2.imwrite('images/{}.jpg'.format(i), d)
    print("Created an image from every frame in the array and stored images in images/<num>.png")

def imageResizing(dim):
    max = len(os.listdir("images"))
    pool = multiprocessing.Pool(processes = 4)
    pool.map(resizeImages, ((i, dim) for i in range(max)))
    print("Images resized.")

def resizeImages(args):
    num = len(os.listdir("images"))
    im = PIL.Image.open("imagesOutPng/{}.png".format(args[0]))
    out = im.resize(args[1])
    out.save("imagesOutPng/{}.png".format(args[0]))

def byint(elem):
    return int(elem[0:elem.index('.png')])

def combineImages(name, fps):
    video_name = 'output/{}.mov'.format(name)
    images = [img for img in os.listdir("imagesOutPng") if img.endswith(".png")]
    images = sorted(images, key = byint)
    frame = cv2.imread("imagesOutPng/" + images[0])
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width,height))
    for image in images:
        video.write(cv2.imread("imagesOutPng/" + image))
    cv2.destroyAllWindows()
    video.release()
    print("Created final video using the ASCII text png files and store video in output/<filename>.mov")

def covertImageToAscii(fileName, cols, scale):
    image = Image.open(fileName).convert('L')
    width, height = image.size[0], image.size[1]
    tileWidth = width / cols
    tileHeight = tileWidth / scale
    rows = int(height / tileHeight)
    asciiImg = []
    for j in range(rows):
        y1 = int(j * tileHeight)
        y2 = int((j + 1) * tileHeight)
        if j == rows - 1:
            y2 = height
        asciiImg.append("")
        for i in range(cols):
            x1 = int(i * tileWidth)
            x2 = int((i + 1) * tileWidth)
            if i == cols - 1:
                x2 = width
            img = image.crop((x1, y1, x2, y2))
            im = np.array(img)
            w, h = im.shape
            avg = int(np.average(im.reshape(w * h)))
            gsval = greyscale[int((avg * 69) / 255)]
            asciiImg[j] += gsval
    return asciiImg

def imageToAscii(args):
    asciiImg = covertImageToAscii(args[0], args[2], args[3])
    with open(args[1], 'w') as f:
        for row in asciiImg:
            f.write(row + '\n')
