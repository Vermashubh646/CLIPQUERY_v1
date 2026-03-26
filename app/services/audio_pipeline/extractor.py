import subprocess

from app.core.logger import custom_logger

def extract_audio_from_video(video_path: str, output_audio_path: str):
    """
    Runs: ffmpeg -i video.mp4 -vn -acodec libmp3lame -q:a 4 output.mp3 -y
    """
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",                   # No video (faster)
        "-acodec", "libmp3lame", # MP3 codec
        "-q:a", "4",             # Standard quality (128-160kbps)
        "-y",                    # Overwrite file if exists
        output_audio_path
    ]

    try:
        custom_logger.info("Audio is being extracted....")
        subprocess.run(command, check=True, capture_output=True)
        custom_logger.info(f"Audio extracted sucesfully at {output_audio_path}")
        return output_audio_path
    except subprocess.CalledProcessError as e:
        custom_logger.error(f"FFmpeg Error: {e.stderr.decode('utf-8')}")
        raise e

