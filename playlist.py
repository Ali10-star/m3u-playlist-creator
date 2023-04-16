from typing import TextIO
from random import shuffle
import os

# ------------------------- GLOBALS -------------------------
all_items = []  # Contains all paths to files found
PLAYLIST_NAME = ''  # The name of the playlist to be created
USED_DIRECTORY = ''
SHUFFLED = False
INCLUDE = False
EXCLUDE = False
APPEND = False
ACCEPTED_FILE_TYPES = ('.mp3', '.flac', '.wav', '.ogg', '.opus', '.m4a')

# ------------------------- GLOBALS -------------------------


def is_audio(filename: str) -> bool:
    global ACCEPTED_FILE_TYPES
    return filename.endswith(ACCEPTED_FILE_TYPES)


def filter_result(filename: str, filter_str: str) -> bool:
    """Helper to apply the filter to a file.

    Args:
        filename (str): Name of file.
        filter_str (str): Comma-separated string containing the filters

    Returns:
        bool: filter result.
    """
    filters = filter_str.split(',')
    result = False

    for f in filters:
        if (filename.lower()).find(f.lower()) != -1:
            result = True

    return result


def accepted(filename: str, filter_str: str = None) -> bool:
    """Filters the filename when using -f, or the reverse filter -nf

    Args:
        filename (str): Name of the audio file.
        filter_str (str): Comma-separated string containing the filters

    Returns:
        bool: True if it matches the filter, false otherwise.
    """
    if not filter_str:
        return is_audio(filename)

    if INCLUDE:
        return is_audio(filename) and filter_result(filename, filter_str)
    elif EXCLUDE:
        return is_audio(filename) and (not filter_result(filename, filter_str))


def file_path(file: str, path: str, subdir: list[str]) -> str:
    """Get full path to a passed file

    Args:
        file (str): File to find path for.
        path (str): Main path of the file
        subdir (List[str]): The subdirectory of the file, empty if it's in the main directory.

    Returns:
        str: Full path to the file.
    """
    if subdir and file in subdir:
        return os.path.join(path, *subdir, file)
    else:
        return os.path.join(path, file)


def open_file(filename: str) -> TextIO:
    specifier = 'w'  # write
    if APPEND:
        specifier = 'a'  # append to file

    return open(filename, specifier, encoding='utf16')


def parse_folder(filter_str: str = None) -> tuple[int, str]:
    global PLAYLIST_NAME, all_items
    for path, subdir, files in os.walk(USED_DIRECTORY):
        for file in files:
            if accepted(file, filter_str):
                full_file_path = file_path(file, path, subdir)
                all_items.append(full_file_path)

    playlist_path = f'{USED_DIRECTORY}\\{PLAYLIST_NAME}'
    return len(all_items), playlist_path


def create_playlist() -> None:
    """Shuffle the playlist file if specified."""
    global PLAYLIST_NAME, all_items

    if SHUFFLED:
        shuffle(all_items)

    with open_file(f'{USED_DIRECTORY}/{PLAYLIST_NAME}') as output_file:
        for item in all_items:
            output_file.write(item + '\n')
    
    # Reset to run script another time
    all_items = []