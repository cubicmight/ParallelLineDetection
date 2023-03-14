import cv2
import numpy as np

# Load the image
img = cv2.imread('Screen Shot 2023-03-03 at 8.39.18 AM.png')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply edge detection using Canny
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply Hough Transform to detect lines
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)

# Draw the detected lines on the image
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Find the two longest lines
lines = sorted(lines, key=lambda x: x[0][0] - x[0][2])
longest_lines = lines[-2:]

# Calculate the center line
x1, y1, x2, y2 = longest_lines[0][0]
x3, y3, x4, y4 = longest_lines[1][0]

m1 = (y2 - y1) / (x2 - x1)
m2 = (y4 - y3) / (x4 - x3)

cx = int((m1*x1 - y1 - m2*x3 + y3) / (m1 - m2))
cy = int(m1*(cx - x1) + y1)

# Draw the center line on the image
cv2.line(img, (cx, cy), (cx + 100, cy + int(100*m1)), (0, 0, 255), 2)

# Show the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
