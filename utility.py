import os, sys

# WARNING: Keep utility.py in root folder of the project

def get_base_path():
    base_filepath = os.path.abspath(__file__)
    base_dir = os.path.dirname(base_filepath)
    base_path = getattr(sys, '_MEIPASS', base_dir)
    return base_path

def get_path(relative_path):
    base_path = get_base_path()
    return os.path.join(base_path, relative_path)
    