import os
import shutil

from .processors.generate_eng_subtitle import generate_english_subtitle
from .processors.get_eng_audio import extract_specific_audio_track
from .processors.mix_subtitle import mix_subtitle_with_video


class Processor:
    def __init__(self, file_info: tuple[str, str]):
        self.file_id, self.file_path = file_info

    def create_folder(self) -> tuple[str, str]:
        temp_dir = f"./temp/{self.file_id}"
        output_dir = f"./output/{self.file_id}"
        os.makedirs(temp_dir) if not os.path.exists(temp_dir) else None
        os.makedirs(output_dir) if not os.path.exists(output_dir) else None
        return temp_dir, output_dir

    def remove_temp_dir(self):
        temp_dir = f"./temp/{self.file_id}"
        shutil.rmtree(temp_dir)

    def run(self):
        complete_filename = os.path.basename(self.file_path)
        _, output_dir = self.create_folder()

        input_video_file = self.file_path
        output_video_file = f"{output_dir}/{complete_filename}"

        # Stage 1: Get English Audio
        output_audio_file = extract_specific_audio_track(input_video_file, self.file_id)

        # Stage 2: Generate English Subtitle
        subtitle_file = generate_english_subtitle(output_audio_file, self.file_id)

        # Stage 3: Mix Subtitle with Video
        mix_subtitle_with_video(input_video_file, subtitle_file, output_video_file)

        self.remove_temp_dir()
        print("Process completed.")


if __name__ == "__main__":
    cur_dir = os.getcwd()
    file_info = ("aaaaa", os.path.join(cur_dir, "test", "test.mp4"))
    processor = Processor(file_info)
    processor.run()
