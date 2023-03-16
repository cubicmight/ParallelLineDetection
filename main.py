import cv2
import numpy as np

def find_center_of_parallel_lines(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply edge detection using Canny
    edges = cv2.Canny(gray, 50, 200)

    # Apply Hough Transform to detect lines
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

    # Identify the two parallel lines
    #SOMETHING WRONG WITH THE PARALLEL CHECK
    parallel_lines = []
    for line1 in lines:
        for line2 in lines:
            if line1[0][1] != line2[0][1]: # Lines should have the same orientation
                continue
            if np.abs(line1[0][0] - line2[0][0]) < 10: # Lines should be roughly parallel
                continue
            parallel_lines.append((line1, line2))

    # Check if there are no parallel lines or multiple pairs of parallel lines
    if len(parallel_lines) != 1:
        print("lines")
        return img

    # Compute the center of the two parallel lines
    line1, line2 = parallel_lines[0]
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]
    intersection = np.cross((x1, y1, 1), (x2, y2, 1)) * np.cross((x3, y3, 1), (x4, y4, 1))
    intersection = np.array([np.cross((x1, y1, 1), (x2, y2, 1)), np.cross((x3, y3, 1), (x4, y4, 1))])
    center = intersection.mean(axis=0)[:2].astype(int)

    # Draw the lines and center on the image
    cv2.line(img, (line1[0][0], line1[0][1]), (line1[1][0], line1[1][1]), (0, 255, 0), 2)
    cv2.line(img, (line2[0][0], line2[0][1]), (line2[1][0], line2[1][1]), (0, 255, 0), 2)
    cv2.line(img, (line1[0][0], line1[0][1]), (line2[0][0], line2[0][1]), (0, 0, 255), 2)
    cv2.circle(img, tuple(center), 5, (0, 0, 255), -1)

    return img

# Load the image
img = cv2.imread("images/weener.JPG")

# Find the center of parallel lines
result = find_center_of_parallel_lines(img)

# Save the result
cv2.imwrite("result.jpg", result)

# Display the result
cv2.imshow("Result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
