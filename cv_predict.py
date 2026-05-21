import cv2
import numpy as np
import joblib

# 1. Load the trained model
print("Loading model...")
model = joblib.load('mnist_model.pkl')
print("Model loaded!")

# 2. Set up the OpenCV canvas
# We use a 280x280 canvas because 28x28 is too small to draw on comfortably.
# We will scale it down later.
CANVAS_SIZE = 280
canvas = np.zeros((CANVAS_SIZE, CANVAS_SIZE), dtype=np.uint8)
drawing = False
q
# 3. Define the drawing function
def draw(event, x, y, flags, param):
    global drawing
    
    # Left mouse button pressed down
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        # Draw a white circle (255) with radius 12
        cv2.circle(canvas, (x, y), 12, (255), -1)
        
    # Mouse moving while button is pressed
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(canvas, (x, y), 12, (255), -1)
            
    # Left mouse button released
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(canvas, (x, y), 12, (255), -1)

# 4. Create the window and bind the mouse events
window_name = 'Draw a Digit (P: Predict, C: Clear, Q: Quit)'
cv2.namedWindow(window_name)
cv2.setMouseCallback(window_name, draw)

print("\n--- Controls ---")
print("Draw with your mouse.")
print("Press 'P' to Predict.")
print("Press 'C' to Clear canvas.")
print("Press 'Q' to Quit.")

# 5. Main application loop
while True:
    cv2.imshow(window_name, canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):      # Quit
        break
    elif key == ord('c'):    # Clear canvas
        canvas = np.zeros((CANVAS_SIZE, CANVAS_SIZE), dtype=np.uint8)
        print("Canvas cleared.")
    elif key == ord('p'):    # Predict
        # Step A: Resize the 280x280 canvas down to 28x28
        resized_img = cv2.resize(canvas, (28, 28), interpolation=cv2.INTER_AREA)
        
        # Step B: Flatten the 28x28 matrix into a 1D array of 784 pixels
        flattened_img = resized_img.flatten()
        
        # Step C: The model expects a 2D array for predictions, so we wrap it in brackets
        prediction = model.predict([flattened_img])
        
        print(f"\n---> The AI predicts you drew a: {prediction[0]} <---")
        
        # Optional: Show what the 28x28 image looks like to the AI
        # cv2.imshow("What the AI sees", cv2.resize(resized_img, (140, 140), interpolation=cv2.INTER_NEAREST))

cv2.destroyAllWindows()