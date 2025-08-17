import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import cv2
from ultralytics import YOLO

# YOLO model
yolo_model = YOLO("models/best_balltracking.pt")

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

videoPath = "videos/fh_bh_testvid.MOV"

vidcap = cv2.VideoCapture(videoPath)
frame_count = 0
fh_count = 0
bh_count = 0
text_to_display = ""
display_frames_counter = 0
frames_for_display = 10 # Display for 10 frames

while True:
    success, frame = vidcap.read()
    if not success:
        break

    results = yolo_model(frame)
    display_frame = frame.copy()

    """
    the light above my head is being detected as a ball lol, so anything with a y coord
    less than 1000 is probably the light so we want to ignore that
    """
    for obj in results[0].boxes.data:
        x1, y1, x2, y2, conf, cls = obj.tolist()
        if y1 >= 1000 and y2 >= 1000:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.putText(display_frame, "Ball", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 5)

        

    if frame_count % 50 == 0:  # every 10th frame
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
    
    # Display frame
    cv2.imshow('Table Tennis Stroke Classification', display_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    frame_count += 1

vidcap.release()
cv2.destroyAllWindows()