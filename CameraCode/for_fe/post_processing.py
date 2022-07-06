#################################################
# this script is about interconnected photos - it is colour detection based image segmentation that is layered up
# 
# This script starts by choosing a colour
# then uses the colour to do contour detection 
# then layers up the contours

# how does it choose the colour?
# option 1: chooses one movie - creates a new folder - splits frames of movie - then deletes all frames but one

import glob
import argparse
import os, random 
import time
import subprocess

import extract_foreground

movieCount = 1
global movieToImages

def movies_to_frames(input_path, output_path):
    movieCount = 1
    for video in glob.glob(os.path.join(input_path,'*.h264')):
        video_frame_dir = os.path.join(output_path, str(movieCount))
        os.makedirs(video_frame_dir)
        os.system('ffmpeg -i '+str(video)+' -vf fps=5 '+str(video_frame_dir)+'/%04d.png')
        print("Finished converting movie {} to frames".format(movieCount))
        movieCount = movieCount+1
    return 


# all images are generated 
# now to process them using color info
# process will be to load an image and do a 'color picker style algorithm'
# then once a colour range is found - do some contour tracing based on that colour 
# if there is none then the spirit hasn't found anything
# randomImageFilePath = random.choice(os.listdir("/home/pi/gather_season_ferment/movieToImages/"+str(random.randrange(0, movieCount))) #change dir name to whatever
# getColorInfor(randomImageFilePathd)


# to process all images:
def extract_foreground_from_frames(movies_to_frames_dir_path, output_path):
    for x in range(1,movieCount+1):

        extracted_movie_path = os.path.join(output_path, x)
        os.makedirs(extracted_movie_path)

        for frame in glob.glob(os.path.join(movies_to_frames_dir_path, str(x), '*.png')):
            threshold1 = 10
            threshold2 = 20
            min_area = 30

            for i in range(5):
                try:
                    extract_foreground.extract_foreground_from_frame(frame, threshold1, threshold2, min_area, extracted_movie_path)
                    break 
                except:
                    print("Extracting foreground threshold did not work...try new threshold")
                    threshold1 += 15
                    threshold2 += 15


    # cmd = 'python3 extract_foreground.py -i /home/pi/gather_season_ferment/movieToImages/1/0008.png -t1 10 -t2 20 -m 30 '.split()
