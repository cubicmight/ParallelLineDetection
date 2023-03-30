import cv2
import numpy as np

# Load the image
img = cv2.imread('turning_pictures/draw.io_curved_image_1.png')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection to detect edges
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply HoughLinesP transform to detect lines
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=30, minLineLength=0, maxLineGap=50)

if lines is not None:
    # Create empty arrays to store the endpoints of the left and right curves
    left_endpoints = []
    right_endpoints = []

    # Iterate through each line detected by HoughLinesP
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Calculate the slope of the line
        slope = (y2 - y1) / (x2 - x1) if x2 != x1 else 0

        # Check if the slope is within a range corresponding to a curved line
        if slope > 0.5:
            right_endpoints.append((x1, y1))
            right_endpoints.append((x2, y2))
        elif slope < -0.5:
            left_endpoints.append((x1, y1))
            left_endpoints.append((x2, y2))

    # Create arrays of x and y coordinates for each set of endpoints
    left_x = [point[0] for point in left_endpoints]
    left_y = [point[1] for point in left_endpoints]
    right_x = [point[0] for point in right_endpoints]
    right_y = [point[1] for point in right_endpoints]

    if len(left_x) > 0 and len(left_y) > 0:
        # Fit a polynomial curve to the points using numpy's polyfit function
        left_fit = np.polyfit(left_y, left_x, 2)

        # Generate x and y values for plotting the curve
        plot_y = np.linspace(0, img.shape[0] - 1, img.shape[0])
        left_fit_x = left_fit[0] * plot_y ** 2 + left_fit[1] * plot_y + left_fit[2]

        # Convert the x and y coordinates of the curve to integer values
        left_fit_x = np.array(left_fit_x, np.int32)
        plot_y = np.array(plot_y, np.int32)

        # Reshape the x and y coordinates into a format required by cv2.polylines
        left_points = np.array([np.transpose(np.vstack([left_fit_x, plot_y]))])

        # Draw the left curve on the image
        cv2.polylines(img, [left_points], False, (255, 0, 0), 5)
    else:
        print("No left curve detected.")

    if len(right_x) > 0 and len(right_y) > 0:
        # Fit a polynomial curve to the points using numpy's polyfit function
        right_fit = np.polyfit(right_y, right_x, 2)

        # Generate x and y values for plotting the curve
        plot_y = np.linspace(0, img.shape[0] - 1, img.shape[0])
        right_fit_x = right_fit[0] * plot_y ** 2 + right_fit[1] * plot_y + right_fit[2]

        # Convert the x and y coordinates of the curve to integer values
        right_fit_x = np.array(right_fit_x, np.int32)
        plot_y = np.array(plot_y, np.int32)

        # Reshape the x and y coordinates into a format required by cv2.polylines
        right_points = np.array([np.transpose(np.vstack([right_fit_x, plot_y]))])

        # Draw the right curve on the image
        cv2.polylines(img, [right_points], False, (255, 0, 0), 5)
    else:
        print("No right curve detected.")

# Display the image with curves drawn on it
cv2.imshow('Curves Detected', img)

# Wait for user input and then close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
