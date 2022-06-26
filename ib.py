# Importing the necessary packages
import cv2
import numpy as np
import os
path = ''

def ib_image(path):
    # Extract the filename from the path
    filename = path.split('\\')[-1]
    

    print('Image name: ', filename)
    # Read image
    img = cv2.imread(path)
    rgb_planes = cv2.split(img) # split the image into 3 channels
    result_planes = [] # list of result planes
    result_norm_planes = [] # list of normalised result planes

    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))  # dilate the image to remove noise
        bg_img = cv2.medianBlur(dilated_img, 21) # apply median blur to remove noise
        diff_img = 255 - cv2.absdiff(plane, bg_img) # get the difference between the plane and the median blur image
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1) # normalise the image
        result_planes.append(diff_img) # add the result plane to the list
        result_norm_planes.append(norm_img) # add the normalised result plane to the list

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    gray_norm = cv2.cvtColor(result_norm, cv2.COLOR_BGR2GRAY)
    #save the image
    ipath = os.path.join('static/augumentedImages', 'image.png')
    cv2.imwrite(ipath, gray)
    #if image exists print the text
    if os.path.isfile(ipath):
        print("Yes")
        



# Use for loop to iterate through the images in assets\drive-download-20220608T180817Z-001\
# and call the ib_image function

# # import required module
# import os
# # assign directory
# directory = 'assets\drive-download-20220608T180817Z-001'
 
# # iterate over files in
# # that directory
# for filename in os.listdir(directory):
#     f = os.path.join(directory, filename)
#     # checking if it is a file
#     if os.path.isfile(f):
#         path = f
#         ib_image(path)
