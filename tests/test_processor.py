import unittest
from unittest import mock

from processor import Processor


class TestProcessor(unittest.TestCase):
    @mock.patch("os.makedirs")
    @mock.patch("os.path.exists", return_value=False)
    def test_create_folder(self, mock_exists, mock_makedirs):
        processor = Processor(("aaaaa", "/path/to/test.mp4"))
        temp_dir, output_dir = processor.create_folder()
        self.assertEqual(temp_dir, "./temp/aaaaa")
        self.assertEqual(output_dir, "./output/aaaaa")
        mock_makedirs.assert_any_call("./temp/aaaaa")
        mock_makedirs.assert_any_call("./output/aaaaa")

    @mock.patch("shutil.rmtree")
    def test_remove_temp_dir(self, mock_rmtree):
        processor = Processor(("aaaaa", "/path/to/test.mp4"))
        processor.remove_temp_dir()
        mock_rmtree.assert_called_once_with("./temp/aaaaa")

    @mock.patch("processor.extract_specific_audio_track")
    @mock.patch("processor.generate_english_subtitle")
    @mock.patch("processor.mix_subtitle_with_video")
    @mock.patch("processor.Processor.create_folder")
    @mock.patch("processor.Processor.remove_temp_dir")
    def test_run(
        self,
        mock_remove_temp_dir,
        mock_create_folder,
        mock_mix_subtitle_with_video,
        mock_generate_english_subtitle,
        mock_extract_specific_audio_track,
    ):
        mock_create_folder.return_value = ("./temp/aaaaa", "./output/aaaaa")
        processor = Processor(("aaaaa", "/path/to/test.mp4"))
        processor.run()
        mock_extract_specific_audio_track.assert_called_once()
        mock_generate_english_subtitle.assert_called_once()
        mock_mix_subtitle_with_video.assert_called_once()
        mock_remove_temp_dir.assert_called_once()


if __name__ == "__main__":
    unittest.main()
