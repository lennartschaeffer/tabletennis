import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import cv2
from ultralytics import YOLO
import os

# Get the base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "../models")

# YOLO models
ball_tracking_model = YOLO(os.path.join(MODEL_DIR, "best_balltracking.pt"))
paddle_tracking_model = YOLO(os.path.join(MODEL_DIR, "best_paddle.pt"))

# Recreate the model architecture
model = models.resnet18(weights=None)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 2)  # 2 classes: forehand/backhand

model.load_state_dict(torch.load(
    os.path.join(MODEL_DIR, "forehand_backhand_model.pth"), 
    map_location=torch.device('cpu')
))
model.eval()  # set to inference mode

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])


def process_video(video_path):
    """Process a table tennis video and return statistics"""
    vidcap = cv2.VideoCapture(video_path)
    frame_count = 0
    fh_count = 0
    bh_count = 0
    hit_count = 0
    hit_recently = False
    
    while True:
        success, frame = vidcap.read()
        if not success:
            break

        ball_tracking_results = ball_tracking_model(frame)
        paddle_tracking_results = paddle_tracking_model(frame)
        
        
        hit_this_frame = False

        # Check for ball hits
        for obj in ball_tracking_results[0].boxes.data:
            x1, y1, x2, y2, conf, cls = obj.tolist()
            if y1 >= 1000 and y2 >= 1000:  # Filter out lights detected as balls
                for paddle in paddle_tracking_results[0].boxes.data:
                    paddle_x1, paddle_y1, paddle_x2, paddle_y2, conf, cls = paddle.tolist()
                    # If ball is within paddle area
                    if (paddle_x1 < x2 and paddle_x2 > x1 and 
                        paddle_y1 < y2 and paddle_y2 > y1):
                        hit_this_frame = True

        # Count hits
        if hit_this_frame and not hit_recently:
            hit_count += 1
            hit_recently = True
        elif not hit_this_frame:
            hit_recently = False

        # Classify stroke type every 50 frames
        if frame_count % 50 == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            image_tensor = transform(image).unsqueeze(0).to(device) # type: ignore

            with torch.no_grad():
                outputs = model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                classes = ['backhand', 'forehand']
                predicted_class = classes[int(predicted.item())]
                
                if predicted_class == 'forehand':
                    fh_count += 1
                else:
                    bh_count += 1

        frame_count += 1

    vidcap.release()
    
    return {
        "forehand_count": fh_count,
        "backhand_count": bh_count,
        "hit_count": hit_count,
        "frame_count": frame_count
    }