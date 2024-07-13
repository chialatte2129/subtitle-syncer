import os
import shutil
import threading
import uuid
from tkinter import filedialog
from typing import List

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image

from .main import Processor
from .wigets.scrollable_label_btn_frame import FilmData, ScrollableLabelButtonFrame


def modify_filename(input_filename):
    # 分割檔案名稱和副檔名
    root, ext = os.path.splitext(input_filename)

    # 在檔案名稱和副檔名之間插入 [sub]
    modified_filename = f"{root}[sub]{ext}"

    return modified_filename


class FileUploadApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.title("MP4 Subtitle Syncer")
        self.upload_files = []
        self.film_data: List[FilmData] = []
        self.file_paths = []  # 用來儲存已選擇的檔案路徑

        title_label = ctk.CTkLabel(
            master=self,
            text="Subtitle Syncer",
            font=ctk.CTkFont(size=30, weight="bold"),
        )
        title_label.grid(row=0, column=0, padx=10, pady=(40, 20))

        self.upload_button = ctk.CTkButton(
            master=self,
            text="Upload",
            command=self.upload_action,
        )
        self.upload_button.grid(row=1, column=0, padx=10, pady=(10, 10))

        # create scrollable label and button frame
        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(
            master=self,
            film_data=self.film_data,
            command_remove=self.remove_film_action,
            command_download=self.download_file_action,
            width=300,
            corner_radius=0,
        )
        self.scrollable_label_button_frame.grid(
            row=2, column=0, padx=10, pady=(10, 20), sticky="nsew"
        )

        self.process_button = ctk.CTkButton(
            master=self, text="Execute", command=self.process_action
        )
        self.process_button.grid(row=3, column=0, padx=10, pady=(0, 10))

        self.download_button = ctk.CTkButton(
            master=self, text="Download All", command=self.download_all_files_action
        )
        self.download_button.grid(row=4, column=0, padx=10, pady=(0, 20))

    def remove_film_action(self, index):
        self.file_paths.pop(index)

    def upload_action(self):
        # 打開檔案對話框，允許用戶選擇多個檔案
        file_paths = filedialog.askopenfilenames(
            title="Select File", filetypes=[("MP4", "*.mp4")]
        )

        # 顯示選擇的檔案路徑並儲存到 self.file_paths
        if file_paths:
            for file_path in file_paths:
                print("Save to:", file_path)
                file_id = str(uuid.uuid4())
                self.file_paths.append((file_id, file_path))

                # 將檔案名稱加入 ScrollableLabelButtonFrame
                file_name = os.path.basename(file_path)
                self.scrollable_label_button_frame.add_item(file_name, file_id)

    def update_finish_status(self, file_id):
        for item in self.film_data:
            if item["file_id"] == file_id:
                item["status"].configure(text="finish", text_color="green")
                item["download_btn"].configure(state="normal")
                self.update()
                return

    def change_btn_state(self, status: str = "normal"):
        self.upload_button.configure(state=status)
        self.process_button.configure(state=status)
        self.download_button.configure(state=status)
        self.update()

    def process_action(self):
        if not self.file_paths:
            print("Please upload file first")
            return

        self.change_btn_state("disabled")
        thread = threading.Thread(target=self.process_files)
        thread.start()

    def process_files(self):
        try:
            for file_info in self.file_paths:
                Processor(file_info).run()
                self.update_finish_status(file_info[0])
            CTkMessagebox(title="Info", message="Finish")
        except Exception as error:
            print(error)
        finally:
            self.change_btn_state("normal")

    def download_file_action(self, file_id):
        print("In: ", file_id)
        if not len(self.file_paths):
            CTkMessagebox(title="Info", message="Can't find file")
            return

        file_path = ""

        for row in self.file_paths:
            if row[0] == file_id:
                _, file_path = row
                break

        file_name = os.path.basename(file_path)
        # 弹出文件选择对话框
        save_file_path = filedialog.asksaveasfile(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4")],
            initialfile=file_name,
        )

        if save_file_path:
            # Convert file_path object to string
            file_path_str = save_file_path.name

            # Define the path to the source MP4 file in your project directory
            source_file_path = (
                f"./output/{file_id}/{file_name}"  # Replace with your actual file path
            )

            try:
                # Copy the source file to the selected destination
                shutil.copyfile(source_file_path, file_path_str)
                CTkMessagebox(title="Info", message=f"Save to: {file_path_str}")
            except Exception:
                CTkMessagebox(title="Info", message="Fails to save")

    def download_all_files_action(self):
        # Ask the user to select a saving folder
        save_folder = filedialog.askdirectory()

        if not save_folder:
            CTkMessagebox(title="Info", message="No saving folder selected")
            return

        for file_info, film_data in zip(self.file_paths, self.film_data):
            if film_data["status"].cget("text") == "finish":
                continue
            file_id, file_path = file_info
            file_name = os.path.basename(file_path)

            # Define the path to the source MP4 file in your project directory
            source_file_path = (
                f"./output/{file_id}/{file_name}"  # Replace with your actual file path
            )

            # Construct the destination file path
            destination_file_path = os.path.join(
                save_folder, modify_filename(file_name)
            )

            # Copy the source file to the selected destination
            shutil.copyfile(source_file_path, destination_file_path)
        CTkMessagebox(title="Info", message=f"Save to: {destination_file_path}")
        print("下載完成", self.file_paths)
