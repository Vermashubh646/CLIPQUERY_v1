import cv2
import os
import base64
import cv2

def frame_to_base64(frame):
    success, buffer = cv2.imencode(".jpg", frame)
    if not success:
        raise RuntimeError("JPEG encode failed")

    return base64.b64encode(buffer).decode("utf-8")

def extract_frame_at_time(video_path, time_sec, output_path):
    """
    Extracts a single frame from a video at a specific time.

    :param video_path: Path to the video file
    :param time_sec: Time in seconds at which to extract the frame
    :param output_path: Path to save the extracted frame image
    """
   
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if time_sec < 0:
        raise ValueError("Time in seconds must be non-negative.")

    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")

    # Get video FPS 
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps

    if time_sec > duration_sec:
        raise ValueError(f"Time exceeds video duration ({duration_sec:.2f} seconds).")

    # frame index
    frame_index = int(fps * time_sec)

    # Set the video position
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to read the frame at the specified time.")

    cv2.imwrite(output_path, frame)
    cap.release()
    
    print(f"Frame at {time_sec:.2f}s saved to {output_path}")
    return frame
    



