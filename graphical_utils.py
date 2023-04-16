from tkinter import Tk
import customtkinter as ctk


def disable_all(*widgets) -> None:
    for widget in widgets:
        widget.configure(state='disabled')


def enable_all(*widgets) -> None:
    for widget in widgets:
        widget.configure(state='normal')


class CustomWindow(ctk.CTk):
    def __init__(self, fixed_size: tuple[int, int], padding: int):
        super().__init__()
        ctk.set_appearance_mode('System')
        ctk.set_default_color_theme('theme/light-blue.json')
        self.title('M3U Playlist Creator')
        self.geometry(f'{fixed_size[0]}x{fixed_size[1]}')
        self.config(padx=padding, pady=padding)
