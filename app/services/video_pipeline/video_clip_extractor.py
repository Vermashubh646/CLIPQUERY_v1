import subprocess
import sys


def get_video_duration(video_path):
    """Get the duration of the video in seconds using ffprobe."""
    command = [
        "ffprobe", 
        "-v", "error", 
        "-show_entries", "format=duration", 
        "-of", "default=noprint_wrappers=1:nokey=1", 
        video_path
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Could not determine duration: {e}", file=sys.stderr)
        return None


def cut_video_clip(input_path: str, start_time: float, end_time: float, output_path: str):
    """
    Extracts a clip from start_time to end_time.
    Uses stream copying for maximum speed (no re-encoding).
    """
    duration = end_time - start_time
    
    command = [
            "ffmpeg",
            "-ss", str(start_time),
            "-t", str(duration),
            "-i", input_path,
            "-c:v", "libx264", "-preset", "ultrafast", # Fast re-encode
            "-c:a", "copy",
            "-y",
            "-loglevel", "error",
            output_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Clip Error: {e.stderr.decode('utf-8')}", file=sys.stderr)
        
        raise e