import cv2
import matplotlib.pyplot as plt

# read the image
image = cv2.imread("turning_pictures/draw.io_curved_image_1.png")
# convert to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# create a binary thresholded image
_, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
# find the contours from the thresholded image
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# get the bounding rectangles of the top and bottom contours
bounding_rects = [cv2.boundingRect(c) for c in contours]
# sort the bounding rectangles from left to right
bounding_rects = sorted(bounding_rects, key=lambda x: x[0])

# get the midpoints between each corresponding point of the top and bottom contours
midpoints = []
for i in range(len(contours[0])):
    x1, y1 = contours[0][i][0]
    x2, y2 = contours[1][i][0]
    midpoints.append(((x1 + x2) // 2, (y1 + y2) // 2))

# draw the center line using the midpoints
for i in range(len(midpoints)-1):
    x1, y1 = midpoints[i]
    x2, y2 = midpoints[i+1]
    image = cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

# show the image with the center line using matplotlib
plt.imshow(image)
plt.show()
