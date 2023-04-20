import tkinter
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter.messagebox as msg_box
import playlist
from tkinter import filedialog
from help import HELP_MESSAGE, get_result
from graphical_utils import disable_all, enable_all, CustomWindow

# -------------------- GLOBALS -------------------
FILTER_SET = False
FILTER = ''
UI_FONT = ('Open Sans', 12, 'normal')
UI_FONT_BOLD = ('Open Sans', 8, 'bold')
# -------------------- GLOBALS -------------------
window = CustomWindow(fixed_size=(500, 300), padding=10)

# ----------------------------------------------------------------------------------------


def set_used_directory() -> None:
    playlist.USED_DIRECTORY = filedialog.askdirectory()
    chosen_lbl.configure(text = "Selected directory: " + playlist.USED_DIRECTORY)
    create_btn.configure(state = 'normal')


choose_directory_lbl = ctk.CTkLabel(master=window, text='Choose a directory to work on:', font=UI_FONT)
choose_directory_lbl.place(x=0, y=5)

choose_directory_btn = ctk.CTkButton(master=window, text='Choose directory', command=set_used_directory)
choose_directory_btn.place(x=180, y=5)

chosen_lbl = ctk.CTkLabel(master=window, text="", font=('Open Sans', 12, 'normal'))
chosen_lbl.place(x=0, y=35)
# ----------------------------------------------------------------------------------------


# ------------------------------ NAMING THE PLAYLIST ---------------------------------------
def set_playlist_name() -> None:
    playlist.PLAYLIST_NAME = playlist_name_entry.get() + '.m3u'


playlist_name_lbl = ctk.CTkLabel(master=window, text="Choose a name for your playlist file: ", font=UI_FONT)
playlist_name_lbl.place(x=0, y=65)

playlist_name_entry = ctk.CTkEntry(master=window, width=180, height=20, corner_radius=5)
playlist_name_entry.place(x=210, y=65)

playlist_set_btn = ctk.CTkButton(master=window, text='Set', height=22, command=set_playlist_name, width=3)
playlist_set_btn.place(x=400, y=65)


# ----------------------------------------------------------------------------------------


# ----------------------- SCRIPT OPTIONS CHECKBOXES -------------------------------

def shuffle_handler() -> None:
    playlist.SHUFFLED = bool(shuffle_state.get())


def append_handler() -> None:
    playlist.APPEND = bool(append_state.get())


shuffle_state = tkinter.IntVar()
shuffle_chkbox = ctk.CTkCheckBox(master=window, text='Shuffle playlist?',
                                 variable=shuffle_state, command=shuffle_handler)
shuffle_chkbox.place(x=0, y=100)

append_state = tkinter.IntVar()
append_chkbox = ctk.CTkCheckBox(master=window, text='Append to file instead of writing on top.',
                                variable=append_state, command=append_handler)
append_chkbox.place(x=195, y=100)


# ---------------------------------------------------------------------------------------


# -------------------------FILTERING SECTION ---------------------------

def filter_handler() -> None:
    global FILTER_SET
    FILTER_SET = bool(filter_state.get())
    if FILTER_SET:
        enable_all(filter_entry, contains_radio, doesnt_contain_radio)
    else:
        disable_all(filter_entry, contains_radio, doesnt_contain_radio)


filter_state = tkinter.IntVar()
filter_chkbox = ctk.CTkCheckBox(master=window, text='Filter songs by some text: ',
                                variable=filter_state, command=filter_handler)
filter_chkbox.place(x=0, y=150)

filter_entry = ctk.CTkEntry(master=window, width=400, state='disabled')
filter_entry.place(x=0, y=180)

contains_state = tkinter.IntVar()
contains_radio = ctk.CTkRadioButton(master=window, text='Contains', value=0,
                                 variable=contains_state, state='disabled')
contains_radio.place(x=0, y=210)

doesnt_contain_radio = ctk.CTkRadioButton(master=window, text="Doesn't Contain", value=1,
                                       variable=contains_state, state='disabled')
doesnt_contain_radio.place(x=100, y=210)


# ---------------------------------------------------------------------------------------


# ----------------------------- HELP BUTTON ------------------------------------------
def display_help_dialog() -> None:
    msg_box.showinfo(title="Help", message=HELP_MESSAGE)


help_btn = ctk.CTkButton(master=window, text='HELP', command=display_help_dialog)
help_btn.place(x=0, y=250)
# ---------------------------------------------------------------------------------------


# ----------------------------- CREATE BUTTON ------------------------------------------
def create_playlist_handler() -> None:
    global FILTER
    FILTER = filter_entry.get()
    match contains_state.get():
        case 0:
            playlist.INCLUDE = True
            playlist.EXCLUDE = False
        case 1:
            playlist.EXCLUDE = True
            playlist.INCLUDE = False
    found_count, playlist_path = playlist.parse_folder(FILTER)
    playlist.create_playlist()
    msg_box.showinfo(title="Done", message=get_result(found_count, playlist_path))


create_btn = ctk.CTkButton(master=window, text='Create Playlist!',
                        command=create_playlist_handler,
                        state='disabled')
create_btn.place(x=340, y=250)
# ----------------------------------------------------------------------------------------

window.mainloop()
