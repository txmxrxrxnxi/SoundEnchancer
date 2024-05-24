import os
import ctypes
from pathlib import Path

import re


def make_file_hidden(filepath: str) \
    -> None:
    """
    Makes a file hidden.
    
    Parameters:
        filepath (str): The path to the file that should be made hidden.

    Returns:
        None
    """
    
    # For Windows
    if os.name == 'nt':
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ret = ctypes.windll.kernel32.SetFileAttributesW(filepath, FILE_ATTRIBUTE_HIDDEN)
        if not ret:
            raise Exception(f'Failed to hide file {filepath}.')
    
    # For Unix, Linux, MacOS
    else:
        dir_name, file_name = os.path.split(filepath)
        hidden_file = os.path.join(dir_name, '.' + file_name)
        os.rename(filepath, hidden_file)

    return

def create_temp_file(filename: str) \
    -> str:
    """
    Creates a temporary file with the same name and extension as the input file, 
    but with "_temp" appended to the name.

    Args:
        filename (str): The name of the file for which a temporary file should be created.

    Returns:
        str: The path to the created temporary file.
    """

    dir_name, file_name = os.path.split(filename)
    base_name, ext = os.path.splitext(file_name)
    temp_file_name = os.path.join(dir_name, base_name + "_temp" + ext)
    Path(temp_file_name).touch()
    return temp_file_name

def delete_temp_file(tempfilename: str) \
    -> None:
    """
    Deletes a temporary file if it exists. If not, does not do anything.

    Args:
        tempfilename (str): The path to the temporary file that should be deleted.

    Returns:
        None.
    """

    if os.path.exists(tempfilename):
        try:
            os.remove(tempfilename)
        except PermissionError:
            pass

def strip_markdown_syntax(text: str) \
    -> str:
    """
    Strips Markdown syntax elements to a raw text.

    Args:
        text (str): The text to strip.

    Returns:
        str: stripped text.
    """
    patterns = {
        r'\*\*(.*?)\*\*': r'\1',  # Bold
        r'\*(.*?)\*': r'\1',      # Italic
        r'__(.*?)__': r'\1',      # Bold
        r'_(.*?)_': r'\1',        # Italic
        r'\#\s*(.*?)\n': r'\1\n', # Headers
        r'\>(.*?)\n': r'\1\n',    # Blockquotes
        r'\`(.*?)\`': r'\1',      # Inline code
    }

    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text)
    
    return text.strip()

def read_markdown(filepath: str) \
    -> str:
    """
    Reads a markdown into HRML data.

    Args:
        filepath (str): The path to the markdown file.

    Returns:
        str: HTML str.
    """

    with open(filepath, 'r', encoding='utf-8') as file:
        markdown_content = file.read()

    cleaned_content = strip_markdown_syntax(markdown_content)
    return cleaned_content
