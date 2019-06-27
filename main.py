from functions import *
import os

filename = "obiwan"
filetype = "mp4"
dim = (1280, 546) # height, width
fps = 30 # frames per second of input video

folders = ['data', 'images', 'imagesOut', 'imagesOutPng', 'output']
for folder in folders:
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

cleanFolders()
getVideoArray("{}.{}".format(filename, filetype))
getImages("array.npy")
getAscii()
convertImages()
imageResizing(dim)
combineImages("{}".format(filename), fps)
