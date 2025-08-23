import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import cv2
from ultralytics import YOLO

# YOLO models
ball_tracking_model = YOLO("models/best_balltracking.pt")
paddle_tracking_model = YOLO("models/best_paddle.pt")

# Recreate the model architecture
model = models.resnet18(weights=None)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 2)  # 2 classes: forehand/backhand

model.load_state_dict(torch.load("models/forehand_backhand_model.pth", map_location=torch.device('cpu')))
model.eval()  # set to inference mode

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

"""
opencv stuff
"""

def get_table_contour(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # green table surface
    lower_green = (35, 40, 40)
    upper_green = (85, 255, 255)
    mask_green = cv2.inRange(hsv, lower_green, upper_green) # type: ignore

    # white lines 
    lower_white = (0, 0, 200)
    upper_white = (180, 40, 255)
    mask_white = cv2.inRange(hsv, lower_white, upper_white) # type: ignore

    # Combine both
    mask = cv2.bitwise_or(mask_green, mask_white)

    # Morphological closing to bridge over white gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    # Take largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Approximate contour to polygon
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # If it's not a quadrilateral, take convex hull to clean up
    if len(approx) != 4:
        approx = cv2.convexHull(largest_contour)

    return approx


videoPath = "videos/fh_bh_testvid.MOV"

vidcap = cv2.VideoCapture(videoPath)
frame_count = 0
fh_count = 0
bh_count = 0
text_to_display = ""
display_frames_counter = 0
frames_for_display = 10 # Display for 10 frames
hit_count = 0
hit_recently = False  # Add this flag

while True:
    success, frame = vidcap.read()
    if not success:
        break

    ball_tracking_results = ball_tracking_model(frame)
    paddle_tracking_results = paddle_tracking_model(frame)
    
    display_frame = frame.copy()
    
    if frame_count == 0:
        table_contour = get_table_contour(frame)
        
    if table_contour is not None:
        cv2.drawContours(display_frame, [table_contour], -1, (0, 255, 0), 3)

    hit_this_frame = False
    """
    the light above my head is being detected as a ball lol, so anything with a y coord
    less than 1000 is probably the light so we want to ignore that
    """
    for i,obj in enumerate(ball_tracking_results[0].boxes.data):
        x1, y1, x2, y2, conf, cls = obj.tolist()
        if y1 >= 1000 and y2 >= 1000:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.putText(display_frame, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5)
            # get paddle coordinates
            for i, paddle in enumerate(paddle_tracking_results[0].boxes.data):
                paddle_x1, paddle_y1, paddle_x2, paddle_y2, conf, cls = paddle.tolist()
                paddle_x1, paddle_y1, paddle_x2, paddle_y2 = map(int, [paddle_x1, paddle_y1, paddle_x2, paddle_y2])
                # if the ball is within the paddle's x coordinates
                if paddle_x1 < x2 and paddle_x2 > x1 and paddle_y1 < y2 and paddle_y2 > y1:
                    # Ball is within paddle area
                    hit_this_frame = True

    if hit_this_frame and not hit_recently:
        cv2.putText(display_frame, "Hit!", (100, 700), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 5)
        hit_count += 1
        hit_recently = True
    elif not hit_this_frame:
        hit_recently = False
        
    for obj in paddle_tracking_results[0].boxes.data:
        x1, y1, x2, y2, conf, cls = obj.tolist()
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
        cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(display_frame, "Paddle", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 5)

    if frame_count % 50 == 0:  # every 50th frame
        # Convert OpenCV BGR -> RGB for model
        frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        # Convert NumPy array to PIL Image
        image = Image.fromarray(frame_rgb)
        
        # Apply transform, convert image to PyTorch tensor
        image_tensor = transform(image).unsqueeze(0).to(device)  # type: ignore

        model.eval()
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1) # get probability distribution
            confidence, predicted = torch.max(probabilities, 1)
            classes = ['backhand', 'forehand']
            predicted_class = classes[int(predicted.item())]
            if predicted_class == 'forehand':
                fh_count += 1
            else:
                bh_count += 1
            display_frames_counter = frames_for_display  # Reset display counter
            confidence_score = confidence.item()

        # Draw prediction on frame (original BGR frame for display)
        text_to_display = f"{predicted_class}: {confidence_score * 100:.2f}%"

    if display_frames_counter > 0:
        if text_to_display:
            cv2.putText(display_frame, text_to_display, (30, 200), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 5)
        display_frames_counter -= 1
    else:
        text_to_display = "" # Clear text when counter reaches 0
            
    # Display counts
    cv2.putText(display_frame, f"Forehand: {fh_count}", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 5)
    cv2.putText(display_frame, f"Backhand: {bh_count}", (100, 500), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 5)
    cv2.putText(display_frame, f"Hits: {hit_count}", (300, 600), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 5)
    
    # Display frame
    cv2.imshow('Table Tennis Stroke Classification', display_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    frame_count += 1

vidcap.release()
cv2.destroyAllWindows()

