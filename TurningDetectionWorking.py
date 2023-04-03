import cv2
import numpy as np

# Read image
image = cv2.imread('turning_pictures/draw.io_curved_image_1.png')

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply HoughLinesP method to
# to directly obtain line end points
lines_list = []
lines = cv2.HoughLinesP(
    edges,  # Input edge image
    1,  # Distance resolution in pixels
    np.pi / 180,  # Angle resolution in radians
    threshold=0,  # Min number of votes for valid line
    minLineLength=0,  # Min allowed length of line
    maxLineGap=10  # Max allowed gap between line for joining them
)

# Iterate over points
for points in lines:
    # Extracted points nested in the list
    x1, y1, x2, y2 = points[0]
    # Draw the lines joing the points
    # On the original image
    cv2.line(image, (x1, y1), (x2, y2), (255, 0, 255), 2)
    # Maintain a simples lookup list for points
    lines_list.append([(x1, y1), (x2, y2)])

longest_lines = sorted(lines, key=lambda x: x[0][2] - x[0][0], reverse=True)[:10]
x1, y1, x2, y2 = longest_lines[0][0]
x3, y3, x4, y4 = longest_lines[1][0]
center_x = int((x1 + x2 + x3 + x4) / 4)
center_y = int((y1 + y2 + y3 + y4) / 4)
print("Center line coordinate point 1: ({}, {})".format(center_x, center_y))
print(x1, x2, y1, y2)
cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
# x12, y12, x22, y22 = longest_lines[4][0]
# x32, y32, x42, y42 = longest_lines[5][0]
# center_x2 = int((x12 + x22 + x32 + x42) / 4)
# center_y2 = int((y12 + y22 + y32 + y42) / 4)
# print("Center line coordinate point 2: ({}, {})".format(center_x2, center_y2))
# print(x12, x22, y12, y22)
# cv2.circle(image, (671, center_y2), 5, (0, 0, 255), -1)


cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

