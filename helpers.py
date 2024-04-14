import os
import ctypes


def make_file_hidden(filepath: str) -> None:
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

def create_temp_file(filename: str) -> str:
    """
    Creates a temporary file with the same name and extension as the input file, 
    but with "_temp" appended to the name. The temporary file is then made hidden.

    Args:
        filename (str): The name of the file for which a temporary file should be created.

    Returns:
        str: The path to the created temporary file.
    """

    dir_name, file_name = os.path.split(filename)
    base_name, ext = os.path.splitext(file_name)
    temp_file_name = os.path.join(dir_name, base_name + "_temp" + ext)

    with open(temp_file_name, 'w') as _:
        pass

    make_file_hidden(temp_file_name)
    return temp_file_name

def delete_temp_file(tempfilename: str) -> None:
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
