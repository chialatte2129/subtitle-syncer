from typing import Callable, Dict, List, Union

import customtkinter as ctk
from PIL import Image

FilmData = Dict[str, Union[str, ctk.CTkLabel, ctk.CTkButton]]


class ScrollableLabelButtonFrame(ctk.CTkScrollableFrame):
    def __init__(
        self,
        master,
        film_data: List[FilmData] = [],
        command_remove: Callable = None,
        command_download: Callable = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.command_download = command_download
        self.command_remove = command_remove
        self.radiobutton_variable = ctk.StringVar()
        self.film_data = film_data

    def add_item(self, item, file_id, image=None):
        label = ctk.CTkLabel(
            self, text=item, image=image, compound="left", padx=5, anchor="w"
        )
        status_label = ctk.CTkLabel(
            self,
            text="waiting",
            image=image,
            text_color="grey",
            compound="left",
            padx=10,
            anchor="w",
        )

        delete_btn_image = ctk.CTkImage(Image.open("static/remove.png"), size=(20, 20))
        download_btn_image = ctk.CTkImage(
            Image.open("static/download.png"), size=(20, 20)
        )

        download_btn = ctk.CTkButton(
            self, text="", image=download_btn_image, width=50, height=24
        )
        remove_btn = ctk.CTkButton(
            self, text="", image=delete_btn_image, width=50, height=24
        )
        if self.command_download is not None:
            download_btn.configure(command=lambda: self.command_download(file_id))

        if self.command_remove is not None:
            remove_btn.configure(command=lambda: self.remove_item(file_id))

        cur_row = len(self.film_data)
        label.grid(row=cur_row, column=0, pady=(0, 10), sticky="w")
        status_label.grid(row=cur_row, column=1, pady=(0, 10), sticky="w")
        remove_btn.grid(row=cur_row, column=2, pady=(0, 10), padx=0)
        download_btn.grid(row=cur_row, column=3, pady=(0, 10), padx=5)

        self.film_data.append(
            {
                "file_id": file_id,
                "file_name": label,
                "status": status_label,
                "remove_btn": remove_btn,
                "download_btn": download_btn,
            }
        )

    def remove_item(self, file_id):
        for i in range(len(self.film_data)):
            row = self.film_data[i]
            if file_id == row["file_id"]:
                row["file_name"].destroy()
                row["status"].destroy()
                row["remove_btn"].destroy()
                row["download_btn"].destroy()
                self.film_data.pop(i)
                self.command_remove(i)
                return
