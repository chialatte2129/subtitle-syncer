import multiprocessing
import os
import shutil

import customtkinter as ctk

from subtitle_adder.gui import FileUploadApp

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app: ctk.CTk = FileUploadApp()

    def on_closing():
        clear_folders = ("./temp", "./output")
        for folder in clear_folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
