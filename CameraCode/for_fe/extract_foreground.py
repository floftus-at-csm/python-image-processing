####################################
# this code should take an image and run a foreground subtraction on it

#taken from here:
# https://debuggercafe.com/image-foreground-extraction-using-opencv-contour-detection/


import numpy as np
import cv2
import argparse
import serial
import imutils
# from utils import show, apply_new_background, find_largest_contour


def find_largest_contour(image, min_area):
    """
    This function finds all the contours in an image and return the largest
    contour area.
    :param image: a binary image
    """
    # add min area here
    image = image.astype(np.uint8)
    # contours, hierarchy
    (_, cnts, _) = cv2.findContours(
        image,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        # areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > min_area:
            largest_contour = max(cnts, key=cv2.contourArea)
            return largest_contour

def extract_foreground_from_frame(input_file_path, threshold1, threshold2, min_area, output_folder_path):

    image = cv2.imread(input_file_path)
    # show('Input image', image)
    # blur the image to smmooth out the edges a bit, also reduces a bit of noise
    # imgBlur = cv2.blur(image,(3, 3))
    imgBlur = cv2.GaussianBlur(image, (5, 5), 0)
    # convert the image to grayscale 
    gray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    # optional switch up
    imgCanny = cv2.Canny(gray, threshold1, threshold2)
    kernel = np.ones((5,5))

    imgDil = cv2.dilate(imgCanny, kernel, iterations = 1)
    contour = find_largest_contour(imgDil, min_area)

    # apply thresholding to conver the image to binary format
    # after this operation all the pixels below 200 value will be 0...
    # and all th pixels above 200 will be 255
    # I think I should change these values to threshold1 and 2
    #ret, gray = cv2.threshold(gray, 200 , 255, cv2.CHAIN_APPROX_NONE)

    # find the largest contour area in the image
    # contour = find_largest_contour(gray)
    image_contour = np.copy(image)
    cv2.drawContours(image_contour, [contour], 0, (0, 255, 0), 2, cv2.LINE_AA, maxLevel=1)
    # show('Contour', image_contour)

    # create a black `mask` the same size as the original grayscale image 
    mask = np.zeros_like(gray)
    # fill the new mask with the shape of the largest contour
    # all the pixels inside that area will be white 
    cv2.fillPoly(mask, [contour], 255)
    # create a copy of the current mask
    res_mask = np.copy(mask)
    res_mask[mask == 0] = cv2.GC_BGD # obvious background pixels
    res_mask[mask == 255] = cv2.GC_PR_BGD # probable background pixels
    res_mask[mask == 255] = cv2.GC_FGD # obvious foreground pixels

    # create a mask for obvious and probable foreground pixels
    # all the obvious foreground pixels will be white and...
    # ... all the probable foreground pixels will be black
    mask2 = np.where(
        (res_mask == cv2.GC_FGD) | (res_mask == cv2.GC_PR_FGD),
        255,
        0
    ).astype('uint8')


    # create `new_mask3d` from `mask2` but with 3 dimensions instead of 2
    new_mask3d = np.repeat(mask2[:, :, np.newaxis], 3, axis=2)
    mask3d = new_mask3d
    mask3d[new_mask3d > 0] = 255.0
    mask3d[mask3d > 255] = 255.0
    # apply Gaussian blurring to smoothen out the edges a bit
    # `mask3d` is the final foreground mask (not extracted foreground image)
    mask3d = cv2.GaussianBlur(mask3d, (5, 5), 0)
    # show('Foreground mask', mask3d)

    # create the foreground image by zeroing out the pixels where `mask2`...
    # ... has black pixels
    foreground = np.copy(image).astype(float)
    foreground[mask2 == 0] = 0
    cv2.imshow('Foreground', foreground.astype(np.uint8))

    # TO DO - save the images to disk - TO DO!
    save_name = os.path.basename(input_file_path).strip(".png")

    cv2.imwrite(os.path.join(output_folder_path, f"{save_name}_foreground.png"), foreground)
    cv2.imwrite(os.path.join(output_folder_path, f"{save_name}_foreground_mask.png"), mask3d)
    # cv2.imwrite(f"outputs/{save_name}_contour.png", image_contour)

