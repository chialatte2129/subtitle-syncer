import re
import subprocess


def extract_stream_info(ffprobe_output):
    stream_blocks = re.findall(
        r"\[STREAM\](.*?)\[/STREAM\]", ffprobe_output, re.DOTALL
    )

    stream_info_list = []
    for stream_block in stream_blocks:
        stream_info = {}
        lines = stream_block.strip().split("\n")
        for line in lines:
            key, value = re.match(r"\s*(\S+)=(.*)", line).groups()
            stream_info[key] = value
        stream_info_list.append(stream_info)

    return stream_info_list


def extract_specific_audio_track(input_file, file_id) -> str:
    output_file = f"./temp/{file_id}/audio."
    stream_info_cmd = [
        "source/ffmpeg/ffprobe.exe",
        "-show_streams",
        "-i",
        input_file,
    ]

    result = subprocess.run(stream_info_cmd, capture_output=True, text=True)
    audio_streams = extract_stream_info(result.stdout)

    track_index = 0
    for stream in audio_streams:
        if (stream["codec_name"] == "mp3" or stream["codec_name"] == "aac") and stream[
            "TAG:language"
        ] == "eng":
            track_index = int(stream["index"]) - 1
            output_file += stream["codec_name"]
            break

    # Run FFmpeg command to extract a specific audio track to an output file
    ffmpeg_command = [
        "source/ffmpeg/ffmpeg.exe",
        "-i",
        input_file,
        "-map",
        f"0:a:{track_index}",
        "-c",
        "copy",
        output_file,
    ]
    subprocess.run(ffmpeg_command)
    return output_file


if __name__ == "__main__":
    # Example usage
    input_file_path = "tests/data/sample_speech.mp4"
    extract_specific_audio_track(input_file_path, "aaa")
