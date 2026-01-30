from scenedetect import detect, ContentDetector, AdaptiveDetector

def get_scene_keyframes(video_path):
    
    scene_list = detect(video_path, AdaptiveDetector())
    
    keyframes = []
    for scene in scene_list:
        start, end = scene
        mid_point = (start.get_seconds() + end.get_seconds()) / 2
        keyframes.append(mid_point)
        
    return keyframes

