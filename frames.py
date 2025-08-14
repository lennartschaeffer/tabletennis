import cv2
import os

video_dir = "videos"
output_dir = "dataset"
os.makedirs(output_dir, exist_ok=True)

for video_file in os.listdir(video_dir):
    label = "forehand" if "forehand" in video_file else "backhand"
    label_dir = os.path.join(output_dir, label)
    os.makedirs(label_dir, exist_ok=True)
    
    vidcap = cv2.VideoCapture(os.path.join(video_dir, video_file))
    frame_count = 0
    saved_count = 0

    while True:
        success, frame = vidcap.read()
        if not success:
            break
        if frame_count % 10 == 0:  # every 10th frame
            img_path = os.path.join(label_dir, f"{video_file}_{saved_count}.jpg")
            cv2.imwrite(img_path, frame)
            saved_count += 1
        frame_count += 1
    vidcap.release()
