import subprocess


def mix_subtitle_with_video(video_file, subtitle_file, output_file):
    # FFmpeg command to overlay subtitles on the video
    ffmpeg_command = [
        "source/ffmpeg/ffmpeg.exe",
        "-i",
        video_file,
        "-i",
        subtitle_file,
        "-map",
        "0",
        "-map",
        "1",
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        "-c:s",
        "mov_text",
        "-metadata:s:s:0",
        "language=eng",
        output_file,
    ]
    print(ffmpeg_command)
    subprocess.run(ffmpeg_command)


if __name__ == "__main__":
    mix_subtitle_with_video(
        "tests/data/test_film.mp4",
        "tests/data/test_subtitle.srt",
        "test_result[sub].mp4",
    )
