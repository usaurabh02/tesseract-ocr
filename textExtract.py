# Import required packages
import cv2
import os
import pytesseract

#Use matplotlib to display the image
def display(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def textExtract(path):
    # Mention the installed location of Tesseract-OCR in your system

    # import ocrspace
    # api = ocrspace.API()
    
    # Read image from which text needs to be extracted
    img = cv2.imread(path)

    
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    # display_image_matplotlib(rect_kernel)
    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
    # display_image_matplotlib(dilation)

    
    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                    cv2.CHAIN_APPROX_NONE)
    

    # Creating a copy of image
    im2 = img.copy()

    #Extract text from the image using api.ocr_file

    # text = api.ocr_file(path)
   
    # A text file is created and flushed
    file_path = os.path.join('static/healthRecords', 'recognized.txt')
    file = open(file_path, "w+")
    # file.write(text)
    file.close()

    
    # pytesseract.pytesseract.tesseract_cmd = "app/eng.traineddata"
    



    



    
    # Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
    i = 1
    for cnt in contours:
        
        x, y, w, h = cv2.boundingRect(cnt) # Find the bounding rectangle

        
        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)   # a green rectangle is drawn
 
        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]                               # a cropped rectangle is made
        #Save each cropped image in assets\cropped folder
        imag = 'cropped' + str(i) + '.png'
        ipath = os.path.join('static/assets/croppedimages', imag )
        cv2.imwrite(ipath, cropped)
        
        f_path = os.path.join('static/healthRecords','recognized.txt')
        file = open(f_path, "a")
        
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)                   # OCR text extraction
        
        # Appending the text into file
        file.write(text)
        
        i = i + 1
        # Close the file
        file.close()
       
    
    #Save rect images
    cv2.imwrite("static\\BoundingBoxes\\rect.jpg", rect)
