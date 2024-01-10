import time

import torch

from subtitle_adder.processors.packages.my_whisper import load_model


def seconds_to_srt_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{seconds:.3f}".replace(".", ",")


def generate_english_subtitle(audio_file, file_id) -> str:
    start_time = time.time()
    output_subtitle_file = f"./temp/{file_id}/audio.srt"
    model_size = "base.en"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model(model_size, device=device)

    transcribe = model.transcribe(audio_file)
    segments = transcribe["segments"]

    with open(output_subtitle_file, "w", encoding="utf-8") as subtitle_file:
        for segment in segments:
            start_timestamp = seconds_to_srt_time(segment["start"])
            end_timestamp = seconds_to_srt_time(segment["end"])
            text = segment["text"].strip()
            segment_index = segment["id"] + 1
            subtitle_line = (
                f"{segment_index}\n{start_timestamp} --> {end_timestamp}\n{text}\n\n"
            )
            subtitle_file.write(subtitle_line)

    print(f"Time taken: {(time.time() - start_time) * 10 **3 * 0.001} second")
    return output_subtitle_file


if __name__ == "__main__":
    audio_file_path = "tests/data/audio.aac"
    generate_english_subtitle(audio_file_path, "aaa")
