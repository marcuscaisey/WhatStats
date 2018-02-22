from glob import glob
import os
from zipfile import ZipFile


def extract_chat_log():
    """Extract chat log from chat log zip in temp folder."""
    chat_log_zip =  glob('temp\*.zip')[0]
    with ZipFile(chat_log_zip) as zip_obj:
        zip_obj.extractall(path='temp')
    # os.remove(chat_log_zip)


def get_chat_log_path():
    """Return path of extracted chat log in temp folder."""
    return glob('temp\*.txt')[0]
