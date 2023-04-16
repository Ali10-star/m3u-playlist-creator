HELP_MESSAGE = """Creates an m3u playlist file from a folder.\n
Select the folder you want to create the playlist from then
name your playlist.\n\n
Filter by some text in the file name by using the filter checkbox,
choose 'contains' to include your search terms, or 'doesn't contain' to exclude them.
Pass multiple filters by separating them with commas.\n\n
Use the append checkbox to add to an existing m3u file.
Use the shuffle checkbox to shuffle songs after creating the playlist."""


def get_result(count: int, playlist_path: str) -> str:
    return f'Found {count} files.\nPlaylist can be found at: {playlist_path}'
